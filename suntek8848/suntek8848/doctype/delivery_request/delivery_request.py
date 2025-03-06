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
			return payments, val['rounded_total']
	
def update_sales_order(doc, method=None):
	if doc.workflow_state1 == 'Approved':
		sales_orders = frappe.get_all("Sales Order", filters={"project": doc.custom_project, "docstatus": 1}, fields=["name"])
		if sales_orders:
			for val in sales_orders:
				sales_order_doc = frappe.get_doc("Sales Order", val["name"])
				
				sales_order_doc.payment_schedule = []
				
				for row in doc.custom_payment_schedule:
					new_row = row.as_dict()
					new_row.pop("name", None)
					new_row["parent"] = sales_order_doc.name
					sales_order_doc.append("payment_schedule", new_row)
				
				sales_order_doc.save()
				frappe.db.commit()
	update_approver_field(doc)

def update_approver_field(doc):
	if doc.workflow_state1 == 'Approved':
		frappe.db.set_value('Delivery Request', doc.name, 'custom_approver', doc.modified_by, update_modified=False)

		# for i in frappe.db.get_all('Delivery Request', {'workflow_state1': 'Approved'}, ['name', 'modified_by']):
		# 	frappe.db.set_value('Delivery Request', i['name'], 'custom_approver', i['modified_by'], update_modified=False)

def on_cancel(doc, method=None):
	sales_orders = frappe.get_all("Sales Order", filters={"project": doc.custom_project, "docstatus": 1}, fields=["name"])
	if sales_orders:
		for val in sales_orders:
			sales_order_doc = frappe.get_doc("Sales Order", val["name"])
			
			sales_order_doc.payment_schedule = []
			
			for row in doc.custom_payment_from_sales_order:
				new_row = row.as_dict()
				new_row.pop("name", None)
				new_row["parent"] = sales_order_doc.name
				sales_order_doc.append("payment_schedule", new_row)
			
			sales_order_doc.save()
			frappe.db.commit()

def on_validate(doc, method=None):
	if doc.custom_project:
		if frappe.db.exists("Delivery Request", {"custom_project": doc.custom_project, 'name':("!=", doc.name), "docstatus": ("!=", 2)}):
			frappe.throw(f"A Delivery Request already exists for project {doc.custom_project}")
