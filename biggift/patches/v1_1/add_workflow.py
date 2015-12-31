# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, cint
from biggift.custom_fixtures import get_workflow_action, get_states, get_workflow
from frappe import _, throw, msgprint

def execute(args = None):
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
	for data in states:
		for state, style in data.items():
			if not frappe.db.get_value('Workflow State'):
				wfs = frappe.get_doc({
					'doctype': 'Workflow State',
					'workflow_state_name': state,
					'style': style
				})
				wfs.save(ignore_permissions=True)

def make_workflow():
	for workflow, value in get_workflow().items():
		name = frappe.db.get_value('Workflow', workflow, 'name')
		if name:
			doc = frappe.get_doc('Workflow', name)
			doc.set('states', [])
			doc.set('transitions', [])
		else:
			doc = frappe.get_doc({
					'doctype': 'Workflow',
					'workflow_name': workflow,
					'is_active': 1,
					'document_type': workflow
				})
		add_workflow_state(doc, workflow, value)
		
		doc.save()

def add_workflow_state(doc, doctype, value):
	for states in value:
		action_transition_dict = {}
		for key, state in states.items():
			for data in state:
				doc.append(key, data)
