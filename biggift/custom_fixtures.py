from __future__ unicode_literals
import frappe

def get_workflow_action():
	return ['Accept','Approve','Assign to Courier',
			'Assign to Delivery Boy','Assign to Production Team',
			'Assign to Sales Person','Complete','Delivery to Customer','Modify','Reject','Review']

def get_states():
	return [{'Accepted': 'Success'},{'Accepted By Manufacture': 'Primary'},{'Accepted By Production Team': 'Success'}
				,{'Approved': 'Success'},{'Assign to Courier': 'Info'},{'Assign to Delivery Boy': 'Info'}
				,{'Assign to Production Team': 'Info'},{'Assign to Sales Person': 'Info'},{'Customer Accepted': 'Success'}
				,{'Customer Modified': 'Info'},{'Customer Rejected': 'Danger'},{'Customer Reviewed Quotation': 'Info' }
				,{'Customer Reviewed SAS': 'Info'},{'Delivered to Customer': 'Info'}
				,{'Delivered to Customer by Courier': 'Info'},{'Delivered to Customer by Delivery Boy': 'Info'}
				,{'Delivered to Customer by Sales Person': 'Info'},{'Pending': 'Info'},{'QC Accepted': 'Success'}
				,{'QC Rejected': 'Danger'},{'Quotation ready for review': 'Info'},{'Rejected': 'Danger'}
				,{'Rejected By Production Team': 'Danger'},{'SAS Completed by Production Team': 'Info'}
				,{'Work Order Completed by Production Team': 'Info'}]


def get_workflow():
	return {'Pre Order':[{'states': [{'state': 'Assign to Production Team', 'doc_status': 0, 'allow_edit': 'Sales User'}, 
									{'state': 'Accepted By Production Team', 'doc_status': 0, 'allow_edit': 'Manufacturing User'},
									{'state': 'Rejected By Production Team', 'doc_status': 0, 'allow_edit': 'Manufacturing User'},
									{'state': 'Assign to Courier', 'doc_status': 0, 'allow_edit': 'Sales User'},
									{'state': 'Assign to Sales Person', 'doc_status': 0, 'allow_edit': 'Sales User'},
									{'state': 'Assign to Delivery Boy', 'doc_status': 0, 'allow_edit': 'Delivery Boy'},
									{'state': 'Rejected', 'doc_status': 0, 'allow_edit': 'Sales User'},
									{'state': 'Accepted', 'doc_status': 1, 'allow_edit': 'Sales User'},
									{'state': 'Delivered to Customer', 'doc_status': 0, 'allow_edit': 'Sales User'},
									{'state': 'Delivered to Customer by Delivery Boy', 'doc_status': 0, 'allow_edit': 'Delivery Boy'},
									{'state': 'Delivered to Customer by Courier', 'doc_status': 0, 'allow_edit': 'Sales User'},
									{'state': 'Delivered to Customer by Sales Person', 'doc_status': 0, 'allow_edit': 'Sales User'}]},
						{'transitions':[{'state': 'Assign to Production Team', 'action': 'Accept', 'next_state': 'Accepted By Production Team', 'allow_edit': 'Manufacturing User'},
										{'state': 'Assign to Production Team', 'action': 'Reject', 'next_state': 'Assign to Sales Person', 'allow_edit': 'Manufacturing User'},
										{'state': 'Accepted By Production Team', 'action': 'Assign to Sales Person', 'next_state': 'Assign to Sales Person', 'allow_edit': 'Manufacturing User'},
										{'state': 'Accepted By Production Team', 'action': 'Assign to Courier', 'next_state': 'Assign to Courier', 'allow_edit': 'Manufacturing User'},
										{'state': 'Accepted By Production Team', 'action': 'Assign to Delivery Boy', 'next_state': 'Assign to Delivery Boy', 'allow_edit': 'Manufacturing User'},
										{'state': 'Assign to Sales Person', 'action': 'Delivery to Customer', 'next_state': 'Delivered to Customer by Sales Person', 'allow_edit': 'Sales User'},
										{'state': 'Assign to Courier', 'action': 'Delivery to Customer', 'next_state': 'Delivered to Customer by Courier', 'allow_edit': 'Sales User'},
										{'state': 'Assign to Delivery Boy', 'action': 'Delivery to Customer', 'next_state': 'Delivered to Customer by Delivery Boy', 'allow_edit': 'Delivery Boy'},
										{'state': 'Delivered to Customer by Sales Person', 'action': 'Accept', 'next_state': 'Accepted', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Sales Person', 'action': 'Modify', 'next_state': 'Assign to Production Team', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Sales Person', 'action': 'Reject', 'next_state': 'Rejected', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Courier', 'action': 'Accept', 'next_state': 'Accepted', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Courier', 'action': 'Modify', 'next_state': 'Assign to Production Team', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Courier', 'action': 'Reject', 'next_state': 'Rejected', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Delivery Boy', 'action': 'Accept', 'next_state': 'Accepted', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Delivery Boy', 'action': 'Modify', 'next_state': 'Assign to Production Team', 'allow_edit': 'Sales User'},
										{'state': 'Delivered to Customer by Delivery Boy', 'action': 'Reject', 'next_state': 'Rejected', 'allow_edit': 'Sales User'}
										]}]}


			