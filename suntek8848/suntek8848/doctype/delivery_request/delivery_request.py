# Copyright (c) 2025, gopal@8848digital.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from copy import deepcopy

class DeliveryRequest(Document):
	def validate(self):
		# frappe.errprint(self.modified_by)
		frappe.db.set_value('Delivery Request', self.name, 'custom_approver', self.modified_by, update_modified=False)
	


@frappe.whitelist()
def fetch_sales_payments(project):
	get_sales_order = frappe.db.get_all('Sales Order', {'project': project, 'docstatus': 1}, ['name', 'rounded_total'])

	if get_sales_order:
		for val in get_sales_order:
			payments = frappe.get_all("Payment Schedule", 
					filters={"parent": val['name']}, 
					fields="*"
				)
			return payments, val['rounded_total'], val['name']
	

def update_sales_order(doc, method=None):
	if doc.workflow_state1 != 'Approved by AM':
		return

	sales_orders = frappe.get_all(
		"Sales Order",
		filters={"project": doc.custom_project, "docstatus": 1},
		fields=["name"]
	)

	def update_payment_schedule(target_doc, source_rows, custom_field):
		"""Update the payment schedule and set the custom advance field."""
		target_doc.payment_schedule = []
		for row in source_rows:
			new_row = row.as_dict()
			new_row.pop("name", None)
			new_row["parent"] = target_doc.name
			target_doc.append("payment_schedule", new_row)

		target_doc.set(custom_field, generate_payment_table(doc))
		target_doc.save()

	def generate_payment_table(doc):
		"""Generate an HTML table for payment details."""
		payment_received = doc.get('payment_received_', 0)
		sales_order_amount = doc.get('sales_order_amount', 0)
		payment_amount = (sales_order_amount * payment_received) / 100

		return f"""
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
						<td style="padding: 5px;">{round(float(payment_received), 2)}</td>
						<td style="padding: 5px;">{round(float(payment_amount), 2)}</td>
					</tr>
				</tbody>
			</table>
		</div>
		"""

	if sales_orders and doc.custom_delivery_request_purpose == 'Revised Payment Schedule':
		for sales_order in sales_orders:
			sales_order_doc = frappe.get_doc("Sales Order", sales_order["name"])
			update_payment_schedule(sales_order_doc, doc.custom_payment_schedule, "custom_advance_amount")

			sales_invoices = get_sales_invoices_from_sales_order(sales_order["name"])
			if sales_invoices:
				for invoice in sales_invoices:
					sales_invoice_doc = frappe.get_doc("Sales Invoice", invoice)
					update_payment_schedule(sales_invoice_doc, doc.custom_payment_schedule, "custom_advance_payment")

		frappe.db.commit()					
	update_approver_field(doc)

def update_approver_field(doc):
	if doc.workflow_state1 == 'Approved by AM':
		frappe.db.set_value('Delivery Request', doc.name, 'custom_approver', doc.modified_by, update_modified=False)

		# for i in frappe.db.get_all('Delivery Request', {'workflow_state1': 'Approved'}, ['name', 'modified_by']):
		# 	frappe.db.set_value('Delivery Request', i['name'], 'custom_approver', i['modified_by'], update_modified=False)

def on_cancel(doc, method=None):
	if doc.workflow_state1 == "Rejected by AM" and not doc.cancel_reason:
		frappe.throw("Please enter a reason before cancellation.")

	sales_orders = frappe.get_all(
		"Sales Order",
		filters={"project": doc.custom_project, "docstatus": 1},
		fields=["name"]
	)

	def update_payment_schedule(target_doc, source_rows, custom_field):
		"""Update the payment schedule and reset custom advance field."""
		target_doc.payment_schedule = []
		for row in source_rows:
			new_row = row.as_dict()
			new_row.pop("name", None)
			new_row["parent"] = target_doc.name
			target_doc.append("payment_schedule", new_row)
		
		setattr(target_doc, custom_field, '')
		target_doc.save()

	if sales_orders and doc.custom_delivery_request_purpose == 'Revised Payment Schedule':
		for sales_order in sales_orders:
			sales_order_doc = frappe.get_doc("Sales Order", sales_order["name"])
			update_payment_schedule(sales_order_doc, doc.custom_payment_from_sales_order, "custom_advance_amount")

			sales_invoices = get_sales_invoices_from_sales_order(sales_order["name"])
			for invoice in sales_invoices:
				sales_invoice_doc = frappe.get_doc("Sales Invoice", invoice)
				update_payment_schedule(sales_invoice_doc, doc.custom_payment_from_sales_order, "custom_advance_payment")

		frappe.db.commit()


def on_validate(doc, method=None):
	if doc.custom_project:
		if frappe.db.exists("Delivery Request", {"custom_project": doc.custom_project, 'name':("!=", doc.name), "docstatus": ("!=", 2)}):
			frappe.throw(f"A Delivery Request already exists for project {doc.custom_project}")

def get_sales_invoices_from_sales_order(sales_order_name):
    """Fetch Sales Invoices linked to a Sales Order"""
    sales_invoices = frappe.get_all(
        "Sales Invoice Item",
        filters={"sales_order": sales_order_name, "docstatus": 1},
        fields=["parent"],
        distinct=True
    )
    
    return [si["parent"] for si in sales_invoices]

@frappe.whitelist()
def get_paid_amount(sales_order):
	payments = frappe.db.get_value(
		"Sales Order",
		sales_order,
		"advance_paid"
	)
	amount = payments if payments else 0

	return amount
