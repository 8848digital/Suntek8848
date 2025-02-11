import frappe

def update_outstanding_amount(doc, method=None):
    frappe.errprint('j')
    amount = sum(val.outstanding for val in (doc.payment_schedule or []))
    doc.custom_outstanding = amount
    frappe.db.set_value('Sales Order', doc.name, 'custom_outstanding', amount, update_modified=False)