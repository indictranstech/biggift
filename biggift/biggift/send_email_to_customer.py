from __future__ import unicode_literals
import frappe
import json
from frappe.utils import  get_url
from frappe import _, throw, msgprint
from frappe.utils.user import get_user_fullname
from frappe.utils import cint, flt, cstr, nowdate

@frappe.whitelist()
def send_sas_link_to_customer(sas_id, customer, sas_to):
	args = {'subject_name': 'SAS Form'}
	link = get_url("/sas?sas_id=" + sas_id)
	request_to = sas_to.lower()
	prepare_data_for_mail(link, customer, args, request_to, "SAS")
	return

@frappe.whitelist()
def send_quotation_link_to_customer(quotation_id, customer, quotation_to):
	args = {'subject_name': 'Quotation Form'}
	link = get_url("/quotation?quotation_id=" + quotation_id)
	request_to = quotation_to.lower()
	prepare_data_for_mail(link, customer, args, request_to, "Quotation")

@frappe.whitelist()
def send_deliverynote_link_to_customer(dn_id, customer, delivery_note_to):
	args = {'subject_name': 'Delivery Note Form'}
	link = get_url("/delivery_note?dn_id=" + dn_id)
	request_to = delivery_note_to.lower()
	prepare_data_for_mail(link, customer, args, request_to, "Delivery Note")

def prepare_data_for_mail(link, customer, args, request_to, doctype):
	contact = frappe.db.get_value('Contact', {request_to: customer, 'is_primary_contact': 1}, '*', as_dict=1) if request_to == 'customer' else frappe.db.get_value('Lead', customer, '*', as_dict=1)
	if contact:
		args = customer_args_for_email(contact, link, args) if request_to == 'customer' else lead_args_for_email(contact, link, args)
		args['doctype'] = doctype
		send_login_mail(_(args.get('subject_name')), 'templates/emails/customer_form.html', args)

def customer_args_for_email(contact, link, args):
	args.update({
		'first_name': contact.first_name,
		'last_name': contact.last_name,
		'user_fullname': get_user_fullname(frappe.session['user']),
		'link': link,
		'email_id': contact.email_id
	})

	return args

def lead_args_for_email(contact, link, args):
	args.update({
		'first_name': contact.lead_name,
		'last_name': '',
		'user_fullname': get_user_fullname(frappe.session['user']),
		'link': link,
		'email_id': contact.email_id
	})

	return args	

def send_login_mail(subject, template, args):
	"""send mail with login details"""
	STANDARD_USERS = ("Guest", "Administrator")
	sender = frappe.session.user not in STANDARD_USERS and frappe.session.user or None
	try:
		data = frappe.sendmail(recipients=args.get('email_id'), sender=sender, subject=subject,
			message=frappe.get_template(template).render(args))
		msgprint("Sent email successfully to customer {0}".format(args.get('first_name')))
	except Exception, e:
		msgprint(e)
