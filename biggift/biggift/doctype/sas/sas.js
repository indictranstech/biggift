{% include 'custom_scripts/validate_user.js' %}

frappe.ui.form.on('SAS', 'refresh', function(frm, cdt, cdn){
	var doc = frm.doc
	if (doc.workflow_state == 'QC Accepted' && in_list(user_roles, 'Sales User')){
    	cur_frm.add_custom_button(__('Email SAS to client'), frm.cscript.send_email_to_customer).addClass("btn-primary");
  	}

  	if(doc.docstatus==0 && !doc.__islocal){
    	frm.cscript.validate_user()
  	}

  	if(doc.docstatus ==0 && in_list(user_roles, 'Sales User')){
  		cur_frm.add_custom_button(__('Make Work Order'), frm.cscript.make_work_order).addClass('btn-primary')
  	}

  	if(doc.workflow_state == 'SAS Completed by Production Team' && doc.qc_status!= 'SAS is assigned to QC team'){
		cur_frm.set_value('qc_status', 'SAS is assigned to QC team')
		cur_frm.save()
	}
	if((doc.workflow_state == 'QC Accepted' || doc.workflow_state == 'QC Rejected') && doc.qc_status!='Qc Done'){
		cur_frm.set_value('qc_status', 'Qc Done')
		cur_frm.save()
	}
})

cur_frm.cscript.send_email_to_customer = function(){
	var doc = cur_frm.doc;
	var client = doc.sas_to == 'Customer' ? doc.customer :doc.lead
	
	frappe.call({
		freeze: true,
		method:"biggift.biggift.send_email_to_customer.send_sas_link_to_customer",
		args: {sas_id: doc.name, 'customer': client, 'sas_to': doc.sas_to},
		callback: function(r){
			cur_frm.set_value('email_sent_to_customer', 'Yes')
			cur_frm.save()
		}
	})
}

frappe.ui.form.on('SAS Item', 'sas_image', function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	refresh_field('image_view', d.name, 'sas_item');
})

cur_frm.cscript.make_work_order = function(frm, cdt, cdn){
	frappe.model.open_mapped_doc({
		method: "biggift.biggift.doctype.sas.sas.make_work_order",
		frm: cur_frm
	})
}

cur_frm.add_fetch('customer', 'customer_name', 'customer_name');
cur_frm.add_fetch('lead', 'lead_name', 'customer_name');	