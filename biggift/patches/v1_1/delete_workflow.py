# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, cint
from biggift.custom_fixtures import get_workflow_action, get_states, get_workflow
from frappe import _, throw, msgprint

def execute():
	delete_workflow()
	delete_workflow_states()
	delete_workflow_actions()

def delete_workflow():
	for workflow, value in get_workflow().items():
		frappe.delete_doc("Workflow", workflow)

def delete_workflow_states():
	for state in get_states():
		frappe.db.sql("""delete from `tabWorkflow State` where name="%(name)s" """, {"name": state})	

def delete_workflow_actions():
	for action in get_workflow_action():
		frappe.delete_doc('Workflow Action', action)