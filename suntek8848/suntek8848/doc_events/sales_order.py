import frappe
from suntek_app.suntek.custom.sales_order import make_project, create_discom, create_subsidy, update_opportunity
from frappe.auth import _

def update_outstanding_amount(doc, method=None):
    amount = sum(val.outstanding for val in (doc.payment_schedule or []))
    doc.custom_outstanding = amount
    frappe.db.set_value('Sales Order', doc.name, 'custom_outstanding', amount, update_modified=False)

@frappe.whitelist()
def validate_work_order(sales_order):
    try:
        so = frappe.get_doc("Sales Order", sales_order)

        bom_list = []
        
        if so.project:
            bom_list = frappe.get_all(
                "BOM", filters={"project": so.project}, pluck="name"
            )
        
        if not bom_list:
            bom_list = [item.bom_no for item in so.items if item.bom_no]
        
        if bom_list:
            work_orders = frappe.get_all(
                "Work Order",
                filters={"bom_no": ["in", bom_list]},
                fields=["name", "status", "bom_no", "produced_qty"],
            )

            if not work_orders:
                return {"message": "No Work Order found for the selected BOM(s)."}

            completed_wo = [wo for wo in work_orders if wo.get("status") == "Completed"]

            total_produced_qty = sum(wo.get("produced_qty", 0) for wo in completed_wo)

            if total_produced_qty >= so.total_qty:
                frappe.db.set_value("Sales Order", sales_order, "custom_dispatch_status", "Ready", update_modified=False)
                frappe.db.commit()
                return 'success'
            else:
                frappe.db.set_value("Sales Order", sales_order, "custom_dispatch_status", "Not Ready", update_modified=False)
                return {"message": f"Insufficient production. Only {total_produced_qty} produced out of {so.total_qty}."}
        else:
            return 'success'

    except Exception as e:
        frappe.log_error(f"Error in validate_work_order: {str(e)}", "validate_work_order")
        return {"error": f"Something went wrong: {str(e)}"}

@frappe.whitelist()
def validate_work_order_for_all():
    try:
        sales_orders = frappe.get_all("Sales Order", filters={}, fields=["name"])
        
        for so in sales_orders:
            frappe.call("suntek8848.suntek8848.doc_events.sales_order.validate_work_order", sales_order=so["name"])

        frappe.db.commit()

        return {"message": "Dispatch Status updated for all Sales Orders!"}
    except Exception as e:
        frappe.log_error(f"Error updating Sales Orders: {str(e)}", "validate_work_order_for_all")
        return {"error": f"Something went wrong: {str(e)}"}

def execute():
    import suntek_app.suntek.custom.sales_order
    suntek_app.suntek.custom.sales_order.auto_project_creation_on_submit = custom_auto_project_creation_on_submit

@frappe.whitelist()
def custom_auto_project_creation_on_submit(doc, method):
    if doc.order_type != "Inter State Stock Transfer":
        if doc.docstatus == 1 and not doc.amended_from:
            project_make = None
            if not frappe.db.exists("Project", {"project_name": doc.name}):
                project_make = make_project(doc)
                project_make.custom_poc_person_name = doc.custom_person_name
                project_make.custom_poc_mobile_no = doc.custom_another_mobile_no
                project_make.save()

                if doc.custom_type_of_case == "Subsidy":
                    create_subsidy(project_make)
                    create_discom(project_make)
                elif doc.custom_type_of_case == "Non Subsidy":
                    create_discom(project_make)

        elif doc.amended_from and doc.project:
            project = frappe.get_doc("Project", doc.project)
            project.db_set("sales_order", doc.name)

        update_opportunity(doc)