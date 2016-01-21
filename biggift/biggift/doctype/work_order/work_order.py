# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, flt
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class WorkOrder(Document):
	def on_submit(self):
		self.update_sales_order_no('submit')

	def on_cancel(self):
		self.update_sales_order_no('cancel')

	def update_sales_order_no(self, type_of_trigger):
		value = self.name if type_of_trigger == 'submit' else 'null' 
		frappe.db.sql(""" update `tabSales Order` set work_order_name = '%s' 
			where name = '%s'"""%(value, self.sales_order_no))


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.posting_date = nowdate()
		target.territory = frappe.db.get_value('Customer', source.customer, 'territory')
		target.order_type = 'Sales'
		target.quotation_to = source.work_order_to

	def update_item(source, target, source_parent):
		target.image = source.work_order_attach
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description 
		target.qty = source.qty
		target.status = ''
		target.prevdoc_doctype = source.parenttype
		target.prevdoc_docname = source.parent

	doclist = get_mapped_doc("Work Order", source_name, {
		"Work Order": {
			"doctype": "Quotation"
		},
		"Work Order Item": {
			"doctype": "Quotation Item",
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.posting_date = nowdate()
		target.territory = frappe.db.get_value('Customer', source.customer, 'territory')

	def update_item(source, target, source_parent):
		target.image = source.work_order_attach
		target.image_view = source.wo_image_view
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description 
		target.qty = source.qty - source.delivered_qty
		target.rate = source.rate
		target.against_sales_order = source.prevdoc_docname
		target.so_detail = source.so_detail

	doclist = get_mapped_doc("Work Order", source_name, {
		"Work Order": {
			"doctype": "Delivery Note"
		},
		"Work Order Item": {
			"doctype": "Delivery Note Item",
			"postprocess": update_item,
			"condition": lambda doc: (flt(doc.qty) - flt(doc.delivered_qty)) > 0
		}
	}, target_doc, set_missing_values)

	return doclist