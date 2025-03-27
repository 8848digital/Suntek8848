frappe.ui.form.on('Employee Advance', {
    setup: function(frm) {
        frm.trigger("set_default_advance_type");
    },

    custom_advance_type: function(frm) {
        if (frm.doc.custom_advance_type === 'Other Expenses') {
            frappe.db.get_value('Company', frm.doc.company, 'custom_default_employee_other_expense_account', function(r) {
                if (r && r.custom_default_employee_other_expense_account) {
                    frm.set_value('advance_account', r.custom_default_employee_other_expense_account);
                }
            });
        } else {
            frappe.db.get_value('Company', frm.doc.company, 'default_employee_advance_account', function(r) {
                if (r && r.default_employee_advance_account) {
                    frm.set_value('advance_account', r.default_employee_advance_account);
                }
            });
        }
    },

    set_default_advance_type: function(frm) {
        frm.set_value("custom_advance_type", "Other Expenses")
    }
});