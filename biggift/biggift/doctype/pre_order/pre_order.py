# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PreOrder(Document):
	pass

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	def update_item(source, target, source_parent):
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description
		target.uom = source.uom
		target.qty = source.qty
		target.previous_docname = source.name

	doclist = get_mapped_doc("Pre Order", source_name, {
		"Pre Order": {
			"doctype": "Purchase Order"
		},
		"Pre Order Item": {
			"doctype": "Purchase Order Item",
			"postprocess": update_item
		}
	}, target_doc)

	return doclist

@frappe.whitelist()
def make_sas(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.sas_to = source.type
		target.pre_order_no = source.name

	def update_item(source, target, source_parent):
		target.item_code = source.item_code
		target.item_name = source.item_name
		target.description = source.description 
		target.qty = source.qty

	doclist = get_mapped_doc("Pre Order", source_name, {
		"Pre Order": {
			"doctype": "SAS"
		},
		"Pre Order Item": {
			"doctype": "SAS Item",
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

	return doclist
