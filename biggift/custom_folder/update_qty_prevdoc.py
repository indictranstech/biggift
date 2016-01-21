from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, flt

def update_wo_qty(doc, method):
	for data in doc.items:
		if data.against_sales_order:
			frappe.db.sql(""" update `tabWork Order Item` set delivered_qty = %s
				where prevdoc_docname = "%s" and so_detail = "%s" and docstatus = 1 """%(data.qty, data.against_sales_order, data.so_detail))