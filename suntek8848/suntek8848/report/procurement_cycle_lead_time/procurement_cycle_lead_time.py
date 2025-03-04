# Copyright (c) 2025, gopal@8848digital.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    if data:
        for val in data:
            if val['grn'] == None and val['po_date']:
                dates = (frappe.utils.getdate() - val['po_date'])
                val['po_to_pr_days'] = dates/ 24
            if val['purchase_order'] == None:
                dates = (frappe.utils.getdate() - val['transaction_date'])
                val['mr_to_po_days'] = dates/ 24
                val['po_to_pr_days'] = dates/ 24

    

    return columns, data

def get_columns():
    return [
        {"label": _("Company"), "fieldname": "company", "fieldtype": "Data", "width": 200},
        {"label": _("Material Request ID"), "fieldname": "material_request", "fieldtype": "Link", "options": "Material Request", "width": 200},
        {"label": _("Purpose Type"), "fieldname": "material_request_type", "fieldtype": "Data", "width": 200},
        {"label": _("Date"), "fieldname": "transaction_date", "fieldtype": "Date", "width": 200},
        {"label": _("Required by"), "fieldname": "schedule_date", "fieldtype": "Date", "width": 200},
        {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 200},
        {"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 200},
        {"label": _("MR Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 200},
        {"label": _("UOM"), "fieldname": "stock_uom", "fieldtype": "Data", "width": 80},
        # {"label": _("Stock Qty in UOM"), "fieldname": "stock_qty", "fieldtype": "Float", "width": 100},
        {"label": _("Ordered Qty"), "fieldname": "po_qty", "fieldtype": "Float", "width": 200},
        {"label": _("Received Qty"), "fieldname": "received_qty", "fieldtype": "Float", "width": 200},
        {"label": _("Qty to Receive"), "fieldname": "po_vs_pr_diff", "fieldtype": "Float", "width": 200},
        {"label": _("Pending PO Qty"), "fieldname": "mr_vs_po_diff", "fieldtype": "Float", "width": 200},
        {"label": _("PO No"), "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order", "width": 200},
        {"label": _("PO Creation Date"), "fieldname": "po_date", "fieldtype": "Date", "width": 200},
        {"label": _("GRN No"), "fieldname": "grn", "fieldtype": "Link", "options": "Purchase Receipt", "width": 200},
        {"label": _("GRN Date"), "fieldname": "grn_date", "fieldtype": "Date", "width": 200},
        {"label": _("MR to PO Lead Days"), "fieldname": "mr_to_po_days", "fieldtype": "Int", "width": 250},
        {"label": _("PO to GRN lead Days"), "fieldname": "po_to_pr_days", "fieldtype": "Int", "width": 250},
    ]

def get_data(filters):
    conditions = []
    params = {}

    if filters.get("from_date"):
        conditions.append("mr.transaction_date >= %(from_date)s")
        params["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("mr.transaction_date <= %(to_date)s")
        params["to_date"] = filters["to_date"]

    if filters.get("item_code"):
        conditions.append("mri.item_code = %(item_code)s")
        params["item_code"] = filters["item_code"]

    if filters.get("warehouse"):
        conditions.append("mri.warehouse = %(warehouse)s")
        params["warehouse"] = filters["warehouse"]

    if filters.get("purchase_order"):
        conditions.append("po.name = %(purchase_order)s")
        params["purchase_order"] = filters["purchase_order"]

    if filters.get("purchase_receipt"):
        conditions.append("pr.name = %(purchase_receipt)s")
        params["purchase_receipt"] = filters["purchase_receipt"]

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT 
            mr.name AS material_request,
            mr.transaction_date,
            mr.material_request_type,
            mri.schedule_date,
            mri.item_code,
            mri.item_name,
            mri.description,
            mri.qty,
            mri.stock_uom,
            mri.warehouse,
            pri.received_qty,
            poi.qty AS po_qty,
            mr.company,
            po.name AS purchase_order,
            po.transaction_date AS po_date,
            pr.name AS grn,
            pr.posting_date AS grn_date,
            TIMESTAMPDIFF(DAY, mr.transaction_date, po.transaction_date) AS mr_to_po_days,
            TIMESTAMPDIFF(DAY, po.transaction_date, pr.posting_date) AS po_to_pr_days,
            COALESCE(poi.qty, 0) - COALESCE(pri.qty, 0) AS po_vs_pr_diff,
            COALESCE(mri.qty, 0) - COALESCE(poi.qty, 0) AS mr_vs_po_diff
        FROM 
            `tabMaterial Request Item` AS mri
        JOIN 
            `tabMaterial Request` AS mr ON mri.parent = mr.name
        LEFT JOIN 
            `tabPurchase Order Item` AS poi ON poi.material_request = mr.name AND poi.material_request_item = mri.name
        LEFT JOIN 
            `tabPurchase Order` AS po ON poi.parent = po.name
        LEFT JOIN 
            `tabPurchase Receipt Item` AS pri ON pri.purchase_order = po.name AND pri.purchase_order_item = poi.name
        LEFT JOIN 
            `tabPurchase Receipt` AS pr ON pri.parent = pr.name
        WHERE {where_clause}
        ORDER BY mr.transaction_date DESC
    """


    return frappe.db.sql(query, params, as_dict=True)

