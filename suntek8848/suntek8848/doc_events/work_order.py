import frappe

def update_sales_order_status(self, method):
    if self.stock_entry_type == 'Manufacture' and self.work_order:
        doc = frappe.get_doc('Work Order', self.work_order)
        if not doc.bom_no:
            return
        
        sales_order_items = frappe.get_all(
            "Sales Order Item",
            filters={"bom_no": doc.bom_no},
            fields=["parent"]
        )

        if not sales_order_items:
            return

        sales_orders = list(set(item["parent"] for item in sales_order_items))

        for so in sales_orders:
            work_orders = frappe.get_all(
                "Work Order",
                filters={"bom_no": doc.bom_no},
                fields=["status", "produced_qty"]
            )

            all_completed = sum(wo["produced_qty"] for wo in work_orders if wo["status"] == "Completed")


            if all_completed >= frappe.db.get_value("Sales Order", so, "total_qty"):
                dispatch_status = "Ready"
            else:
                dispatch_status = "Not Ready"
            frappe.db.set_value("Sales Order", so, "custom_dispatch_status", dispatch_status, update_modified=False)
