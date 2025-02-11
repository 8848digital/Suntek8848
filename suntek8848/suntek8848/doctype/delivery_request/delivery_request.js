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
                        response.message.forEach(row => {
                            
                            let child = frm.add_child("custom_payment_from_sales_order");
                            
                            let excluded_fields = ["base_payment_amount", "description", "discount_date", "discount", "discount_type",
                                "discounted_amount", "due_date", "invoice_portion", "outstanding", "paid_amount", "payment_amount", "payment_term"
                            ];
                            Object.keys(row).forEach(key => {
                                if (excluded_fields.includes(key)) {
                                    child[key] = row[key];
                                }
                            });
                        });
                        frm.refresh_field("custom_payment_from_sales_order");
                    }
                });
            }
            
        });
	},
});
