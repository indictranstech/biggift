from __future__ import unicode_literals
import frappe

def new_comment(doc, method):
	if doc.comment_doctype in ['Pre Order', 'Work Order', 'SAS']:
		obj = frappe.get_doc(doc.comment_doctype, doc.comment_docname)
		obj.latest_comment = 'Unread'
		obj.comment_user_name = frappe.session['user']
		obj.save()