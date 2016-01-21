from __futre__ import unicode_literals
import frappe
from frappe.utils import cstr, flt


@frappe.whitelist()
def send_email_to_customer(customer, delivery_note):
	pass