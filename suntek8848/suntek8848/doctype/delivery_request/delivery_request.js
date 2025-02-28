// Copyright (c) 2025, gopal@8848digital.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Delivery Request", {
	refresh(frm) {
        frm.add_custom_button('Get Sales Order Terms', function() {
            if (frm.doc.custom_payment_from_sales_order.length <1){
                frappe.call({
                    method: "suntek8848.suntek8848.doctype.delivery_request.delivery_request.fetch_sales_payments",
                    args: {
                        project: frm.doc.custom_project
                    },
                    callback: function(response) {
                        console.log(response)
                        response.message[0].forEach(row => {
                            
                            let child = frm.add_child("custom_payment_from_sales_order");
                            
                            let excluded_fields = ["base_payment_amount", "description", "discount_date", "discount", "discount_type",
                                "discounted_amount", "due_date", "invoice_portion", "outstanding", "paid_amount", "payment_amount", "payment_term"
                            ];
                            Object.keys(row).forEach(key => {
                                if (excluded_fields.includes(key)) {
                                    child[key] = row[key];
                                }
                            });
                            child['custom_sales_amount'] = response.message[1]
                        });
                        frm.refresh_field("custom_payment_from_sales_order");
                    }
                });
            }
            
        });
	},
});

frappe.ui.form.on('Payment Schedule', {
    payment_amount: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        let total_payment = 0;
        frm.doc.custom_payment_schedule.forEach(r => {
            total_payment += r.payment_amount || 0;
        });

        let sales_amount = frm.doc.custom_payment_from_sales_order[0].custom_sales_amount || 0;

        if (total_payment > sales_amount) {
            frappe.msgprint(`Total Delivery payment cannot exceed Sales Order amount (${sales_amount})`);
            frappe.model.set_value(cdt, cdn, 'payment_amount', 0);
        }
    }
});
