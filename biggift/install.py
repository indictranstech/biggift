from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, cint
from biggift.custom_fixtures import get_workflow_action, get_states, get_workflow
from frappe import _, throw, msgprint

def after_install():
	make_workflow_action()
	make_workflow_state()
	make_workflow()

def make_workflow_action():
	for action in get_workflow_action():
		if not frappe.db.get_value('Workflow Action', action, 'name'):
			wfa = frappe.get_doc({
				'doctype': 'Workflow Action',
				'workflow_action_name': action,
			})
			wfa.save(ignore_permissions=True)

def make_workflow_state():
	states = get_states()
	for state, style in states.items():
		if not frappe.db.get_value('Workflow State'):
			wfs = frappe.get_doc({
				'doctype': 'Workflow State',
				'workflow_state_name': state,
				'style': style
			})
			wfs.save(ignore_permissions=True)

def make_workflow():
	pass



