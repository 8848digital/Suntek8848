import frappe


def update_permissions(user):
    if not user: user = frappe.session.user

    get_name = frappe.db.get_value('Employee', {'user_id': user}, 'name')

    if get_name:
        get_all_reports_to = frappe.db.get_all('Employee', {'reports_to': get_name}, pluck='user_id')

       
        if get_all_reports_to:
            get_all_reports_to += [user]
            return """(`owner` IN ({owners}))""".format(
                owners=", ".join(f"'{user}'" for user in get_all_reports_to)
            )