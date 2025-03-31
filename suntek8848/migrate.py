import frappe

def after_migrate():
    add_select_option()

def add_select_option():
    field = frappe.get_doc("Property Setter", {
        "doc_type": "Sales Order",
        "field_name": "order_type", 
        "property": "options"
    })
    if field:
        existing_options = field.value.split("\n")
        if "Inter State Stock Transfer" not in existing_options:
            existing_options.append("Inter State Stock Transfer")
            field.value = "\n".join(existing_options)
            field.save()