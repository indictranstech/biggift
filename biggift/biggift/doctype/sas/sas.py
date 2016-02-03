# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _, throw, msgprint
from frappe.utils import cint, flt, cstr, nowdate
from frappe.utils.user import get_user_fullname
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from biggift.biggift.custom_methods import get_workflow_state

class SAS(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_sas_details(sas_id):
	response = {'status': False, 'msg':'Error'}
	if sas_id:
		sas = frappe.get_doc('SAS', sas_id)
		if sas.workflow_state == 'QC Accepted':
			response = {
				'status': True,
				'customer_name': sas.customer_name,
				'email_id': frappe.db.get_value('Contact', {'customer': sas.customer}, 'email_id'),
				'sas_item': sas.sas_item
			}
	return response

@frappe.whitelist(allow_guest=True)
def customer_review(args):
	args = json.loads(args)
	get_sas_doc(args)
	return "/"

def get_sas_doc(args):
	sas = frappe.get_doc('SAS', args.get('sas_id'))
	if sas.workflow_state == 'QC Accepted':
		update_customer_review(sas, args)

def update_customer_review(sas, args):
	update_employee_details(sas, args)
	update_sas_status(sas, args.get('completed_list'))
	workflow_state = get_workflow_state(sas.sas_item, args.get('completed_list'))
	sas.workflow_state = workflow_state
	if workflow_state != 'Customer Accepted': sas.email_sent_to_customer = 'Yes'
	sas.save(ignore_permissions=True)
	if sas.workflow_state == 'Customer Accepted':
		sas.submit()

def update_employee_details(sas, args):
	for key, val in args.items():
		if key not in ['completed_list', 'sas_id']:
			setattr(sas, key, val)

def update_sas_status(sas, completed_list):
	for data in sas.sas_item:
		data.status = '<p style="color:red">Rejected</p>'
		if cstr(data.idx) in completed_list:
			data.status = '<p style="color:green">Completed</p>'

@frappe.whitelist()
def make_work_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.order_type = 'Sample'
		target.posting_date = nowdate()
		target.feedback = ""
		target.work_order_to = source.sas_to

	def update_item(source, target, source_parent):
		target.work_order_attach = source.sas_image
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description 
		target.qty = source.qty
		target.prevdoc_doctype = source.parenttype
		target.prevdoc_docname = source.parent
		target.status = ''

	doclist = get_mapped_doc("SAS", source_name, {
		"SAS": {
			"doctype": "Work Order"
		},
		"SAS Item": {
			"doctype": "Work Order Item",
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

	return doclist