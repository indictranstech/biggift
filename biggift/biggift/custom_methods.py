from __future__ import unicode_literals
import frappe
import json
from frappe import _, throw, msgprint
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, cstr, nowdate

@frappe.whitelist(allow_guest=True)
def get_quotation_details(doctype, name):
	response = {'status': False, 'msg':'Error'}
	if name:
		doc = frappe.get_doc(doctype, name)
		if doc.workflow_state == 'Quotation ready for review':
			response = {
				'status': True,
				'email_id': frappe.db.get_value('Contact', {'customer': doc.customer}, 'email_id'),
				'doc': doc,
				'letterhead': frappe.db.get_value('Letter Head', doc.letter_head, 'content')
			}
	return response

@frappe.whitelist(allow_guest=True)
def get_dn_details(doctype, name):
	response = {'status': False, 'error_msg':'ID {0} is unknown'.format(name)}
	if name:
		doc = frappe.get_doc(doctype, name)
		if doc.docstatus == 1:
			response = {
				'status': True,
				'email_id': frappe.db.get_value('Contact', {'customer': doc.customer}, 'email_id'),
				'doc': doc
			}
		else:
			response['error_msg'] = 'Customer has reviewed this form'
	return response	

@frappe.whitelist(allow_guest=True)
def customer_review_on_quotation(args):
	args = json.loads(args)
	get_quotation_doc(args)
	send_thanks_email(args)
	sendmail_to_sales_person(args)
	return "/"

def get_quotation_doc(args):
	doc = frappe.get_doc('Quotation', args.get('quotation_id'))
	if doc.workflow_state == 'Quotation ready for review':
		update_customer_review(doc, args)

def update_customer_review(doc, args):
	update_employee_details(doc, args)
	update_quotation_status(doc, args.get('completed_list'))
	workflow_state = get_workflow_state(doc.items, args.get('completed_list'))
	doc.workflow_state = workflow_state
	doc.save(ignore_permissions=True)
	if doc.workflow_state == 'Customer Accepted':
		doc.submit()

def update_employee_details(doc, args):
	for key, val in args.items():
		if key not in ['completed_list', 'quotation_id']:
			setattr(doc, key, val)

def update_quotation_status(doc, completed_list):
	for data in doc.items:
		data.status = '<p style="color:red">Rejected</p>'
		if cstr(data.idx) in completed_list:
			data.status = '<p style="color:green">Completed</p>'

def send_thanks_email(args):
	msg="""
			Quotation {0} has Confirmed.
			Thanks For Your Confirmation,
			We will come back soon.
		""".format(args.get('quotation_id'))
	
	sub="""Quotation Confirmation"""
	send_email(args.get('employee_id'), msg, sub)

def sendmail_to_sales_person(args):
	msg="""
			Quotation {0} has Confirmed by,
			Customer: {1}
			ID: {2}
		""".format(args.get('quotation_id'), args.get('employee_name'), args.get('employee_id'))
	
	sub="""Quotation Confirmation"""
	send_email(args.get('Sales_person'), msg, sub)

def send_email(emailid, msg, sub):
	frappe.sendmail(emailid, subject=sub, message = msg)

@frappe.whitelist(allow_guest=True)
def customer_review_on_dn(args):
	args = json.loads(args)
	get_dn_doc(args)
	return "/"

def get_dn_doc(args):
	doc = frappe.get_doc('Delivery Note', args.get('dn_id'))
	update_dn_status(doc, args.get('completed_list'))
	doc.save()

def update_dn_status(doc, completed_list):
	for data in doc.items:
		data.customer_review_on_delivery = '<p style="color:red">Not Received</p>'
		if cstr(data.idx) in completed_list:
			data.customer_review_on_delivery = '<p style="color:green">Received</p>'

@frappe.whitelist()
def make_work_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.order_type = 'Sales'
		target.posting_date = nowdate()
		target.feedback = ""
		target.work_order_to = 'Customer'
		target.sales_order_no = source.name

	def update_item(source, target, source_parent):
		target.work_order_attach = frappe.db.get_value('Quotation Item', {'item_code': source.item_code, 'parent': source.prevdoc_docname}, 'image')
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description 
		target.qty = source.qty
		target.rate = source.rate
		target.prevdoc_doctype = source.parenttype
		target.prevdoc_docname = source.parent
		target.status = ''
		target.so_detail = source.name

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Work Order"
		},
		"Sales Order Item": {
			"doctype": "Work Order Item",
			"postprocess": update_item
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges"
		},
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def make_pre_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.type = source.enquiry_from

	def update_item(source, target, source_parent):
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description 
		target.qty = 1

	doclist = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Pre Order"
		},
		"Opportunity Item": {
			"doctype": "Pre Order Item",
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

	return doclist

def get_workflow_state(items, completed_list):
	workflow_state = 'Customer Modified'
	if len(completed_list) == 0 : workflow_state = 'Customer Rejected'
	if len(completed_list) == len(items) : workflow_state = 'Customer Accepted'
	return workflow_state

