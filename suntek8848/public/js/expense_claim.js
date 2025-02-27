frappe.ui.form.on('Expense Claim', {
	setup: function(frm) {
		frm.set_query("employee_advance", "advances", function () {
			return {
				filters: [
					["docstatus", "=", 1],
					["employee", "=", frm.doc.employee],
					["paid_amount", ">", 0],
					["status", "not in", ["Claimed", "Returned", "Partly Claimed and Returned"]],
					["custom_advance_type", "=", 'Other Expenses']
				],
			};
		});

	}
})