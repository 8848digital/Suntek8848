// Copyright (c) 2025, gopal@8848digital.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Delivery Request", {
    onload: function (frm) {
        if (frm.doc.owner) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Employee",
                    filters: { user_id: frm.doc.owner },
                    fields: ["department"]
                },
                callback: function (r) {
                    if (r.message.length > 0) {
                        frm.set_value("department", r.message[0].department);
                    }
                }
            });
        }
    },
	refresh(frm) {
        if (!frm.doc.cancel_reason) {
            frm.toggle_display("cancel_reason", false);
        }
        frm.get_sales_order_terms = function () {
            if (frm.doc.docstatus == 0){
                frappe.call({
                    method: "suntek8848.suntek8848.doctype.delivery_request.delivery_request.fetch_sales_payments",
                    args: {
                        project: frm.doc.custom_project
                    },
                    callback: function(response) {
                        console.log(response)
                        frm.clear_table("custom_payment_from_sales_order");
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
            
        }
        if (frm.doc.custom_delivery_request_purpose == 'Revised Payment Schedule'){
            frm.add_custom_button('Get Sales Order Terms', function() {
                frm.get_sales_order_terms();
            });
        }
        frm.fields_dict.custom_payment_schedule.grid.update_docfield_property("invoice_portion", "read_only", 1);
        frm.fields_dict.custom_payment_schedule.grid.update_docfield_property("payment_term", "reqd", 1);
        
	},
    validate: function(frm) {
        if(frm.doc.custom_delivery_request_purpose != 'Revised Payment Schedule'){
            frm.set_value('sales_order', '')
            frm.set_value('sales_order_amount', '')
            frm.doc.custom_payment_schedule = ''
            frm.doc.custom_payment_from_sales_order = ''
        }
        if (frm.doc.custom_payment_schedule.length > 0){
            let total_payment = 0;
            frm.doc.custom_payment_schedule.forEach(r => {
                total_payment += r.payment_amount || 0;
            });
            total_payment += (frm.doc.sales_order_amount * frm.doc.payment_received_) /100

            let sales_amount = frm.doc.custom_payment_from_sales_order[0].custom_sales_amount || 0;

            if (Math.round(total_payment) != sales_amount) {
                frappe.throw(`Total Delivery payment (${Math.round(total_payment)}) mismatch with Sales Order amount (${Math.round(sales_amount)})`);
            }
        }
    },
    custom_project: function(frm){      
        frappe.call({
            method: "suntek8848.suntek8848.doctype.delivery_request.delivery_request.fetch_sales_payments",
            args: {
                project: frm.doc.custom_project
            },
            callback: function(response) {
                frm.set_value('sales_order', response.message[2])
                frm.set_value('sales_order_amount', response.message[1])
            }
        });
        if (frm.doc.custom_delivery_request_purpose == 'Revised Payment Schedule'){
            frm.get_sales_order_terms();
        }
        let advance = generatePaymentTable(frm.doc)
        frm.set_value('custom_advance',advance)
        fetch_payment(frm)
    },
    custom_delivery_request_purpose: function(frm){
        if(frm.doc.custom_project){
            frm.trigger('custom_project')
        }
        
    },
    before_workflow_action: function (frm) {
        if (frm.doc.workflow_state1 === "Approved by AM" || frm.doc.workflow_state1 === "Waiting for AM Approval" || frm.doc.workflow_state1 === "Waiting for SM Approval") {
            frm.toggle_display("cancel_reason", true);
        }
    }
});

function fetch_payment(frm){
    setTimeout(function () {
        if(frm.doc.sales_order){
            frappe.call({
                method: "suntek8848.suntek8848.doctype.delivery_request.delivery_request.get_paid_amount",
                args: {
                    sales_order: frm.doc.sales_order
                },
                callback: function(response) {
                    frm.set_value('payment_received_', ((response.message)/frm.doc.sales_order_amount)*100)
                    frm.set_value('advance_payment', response.message)
                    frm.set_value('remaining_amount', (frm.doc.sales_order_amount - response.message))
                }
            });
        }
    }, 500);
}

frappe.ui.form.on('Payment Schedule', {
    payment_amount: function(frm, cdt, cdn){
        let row = locals[cdt][cdn];
        if (frm.doc.custom_payment_from_sales_order.length > 0){
            let sales_amount = frm.doc.custom_payment_from_sales_order[0].custom_sales_amount || 0;
            remaining_per = (row.payment_amount / sales_amount) * 100
            frappe.model.set_value(cdt, cdn, 'invoice_portion', remaining_per)
        }else{
            frappe.call({
                method: "suntek8848.suntek8848.doctype.delivery_request.delivery_request.fetch_sales_payments",
                args: {
                    project: frm.doc.custom_project
                },
                callback: function(response) {
                    let sales_amount = response.message[1]|| 0;
                    remaining_per = (row.payment_amount / sales_amount) * 100
                    frappe.model.set_value(cdt, cdn, 'invoice_portion', remaining_per)
                }
            });
        }
        let total_payment = 0;
        if (frm.doc.custom_payment_schedule.length > 0){
            frm.doc.custom_payment_schedule.forEach(r => {
                total_payment += r.payment_amount || 0;
            });
        }
        frm.set_value('remaining_amount', ((frm.doc.sales_order_amount - frm.doc.advance_payment) - total_payment))
    },
    // invoice_portion: function(frm, cdt, cdn){
    //     let row = locals[cdt][cdn];
    //     if (frm.doc.custom_payment_from_sales_order.length > 0){
    //         let sales_amount = frm.doc.custom_payment_from_sales_order[0].custom_sales_amount || 0;
    //         remaining_amount = (sales_amount * row.invoice_portion) /100
    //         frappe.model.set_value(cdt, cdn, 'payment_amount', remaining_amount)
    //     }else{
    //         frappe.call({
    //             method: "suntek8848.suntek8848.doctype.delivery_request.delivery_request.fetch_sales_payments",
    //             args: {
    //                 project: frm.doc.custom_project
    //             },
    //             callback: function(response) {
    //                 console.log(response)
    //                 let sales_amount = response.message[1]|| 0;
    //                 remaining_amount = (sales_amount * row.invoice_portion) /100
    //                 frappe.model.set_value(cdt, cdn, 'payment_amount', remaining_amount)
    //             }
    //         });
    //     }
    //     let total_payment = 0;
    //     if (frm.doc.custom_payment_schedule.length > 0){
    //         frm.doc.custom_payment_schedule.forEach(r => {
    //             total_payment += r.payment_amount || 0;
    //         });
    //     }
    //     frm.set_value('remaining_amount', ((frm.doc.sales_order_amount - frm.doc.advance_payment) - total_payment))
    // },
    custom_payment_schedule_remove:function (frm, cdt, cdn) {
        let total_payment = 0;
        if (frm.doc.custom_payment_schedule.length > 0){
            frm.doc.custom_payment_schedule.forEach(r => {
                total_payment += r.payment_amount || 0;
            });
        }
        frm.set_value('remaining_amount', ((frm.doc.sales_order_amount - frm.doc.advance_payment) - total_payment))
    }
});

function generatePaymentTable(doc) {
    let payment_received = doc.payment_received_ || 0;
    let sales_order_amount = doc.sales_order_amount || 0;
    let payment_amount = (sales_order_amount * payment_received) / 100;

    return `
        <div style="margin: 0; padding: 0; width: 100%; display: flex; align-items: flex-start;">
            <table class="table table-bordered" style="border-collapse: collapse; width: 100%; margin-top: 0;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 5px; text-align: left;">Payment Term</th>
                        <th style="padding: 5px; text-align: left;">Invoice Portion</th>
                        <th style="padding: 5px; text-align: left;">Payment Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 5px;">Advance Amount</td>
                        <td style="padding: 5px;">${parseFloat(payment_received).toFixed(2)}</td>
                        <td style="padding: 5px;">${parseFloat(payment_amount).toFixed(2)}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}