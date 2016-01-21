# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "biggift"
app_title = "biggift"
app_publisher = "New Indictrans"
app_description = "biggift"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "rohit.w@indictranstech.com"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/biggift/css/biggift.css"
# app_include_js = "/assets/biggift/js/biggift.js"

# include js, css files in header of web template
# web_include_css = "/assets/biggift/css/biggift.css"
# web_include_js = "/assets/biggift/js/biggift.js"
setup_wizard_complete = "biggift.patches.v1_1.add_workflow.execute"
# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

fixtures = ['Custom Field']

# before_install = "biggift.install.before_install"
after_install = "biggift.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "biggift.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

doctype_js = {
	"Quotation": ["custom_scripts/quotation.js"],
	"Sales Order": ["custom_scripts/sales_order.js"],
	"Opportunity": ["custom_scripts/opportunity.js"],
	"Delivery Note": ["custom_scripts/delivery_note.js"]
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
	"Delivery Note":{
		"on_submit": "biggift.custom_folder.update_qty_prevdoc.update_wo_qty"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"biggift.tasks.all"
# 	],
# 	"daily": [
# 		"biggift.tasks.daily"
# 	],
# 	"hourly": [
# 		"biggift.tasks.hourly"
# 	],
# 	"weekly": [
# 		"biggift.tasks.weekly"
# 	]
# 	"monthly": [
# 		"biggift.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "biggift.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "biggift.event.get_events"
# }
