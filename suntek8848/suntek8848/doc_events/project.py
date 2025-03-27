import frappe

@frappe.whitelist()
def fetch_sales_order_fields(doc, method):
    if doc.sales_order:
        so = frappe.get_doc("Sales Order", doc.sales_order)
        doc.custom_state = so.custom_suntek_state
        doc.custom_branch = so.branch

        doc.save()