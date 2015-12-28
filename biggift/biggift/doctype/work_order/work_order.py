# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class WorkOrder(Document):
	pass


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