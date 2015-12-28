frappe.ui.form.on('Quotation', 'refresh', function(frm, cdt, cdn){
	var doc = frm.doc; 
	if(doc.workflow_state == 'Quotation ready for review' && in_list(user_roles, 'Sales User'))
		cur_frm.add_custom_button(__("Send Quotation to Customer"), frm.cscript.send_quotation).addClass('btn-primary')
})

cur_frm.cscript.send_quotation = function(){
	var doc = cur_frm.doc
	var client = doc.quotation_to == 'Customer' ? doc.customer :doc.lead

	frappe.call({
		freeze: true,
		method:"biggift.biggift.send_email_to_customer.send_quotation_link_to_customer",
		args: {quotation_id: doc.name, 'customer': client, 'quotation_to': doc.quotation_to}
	})
}