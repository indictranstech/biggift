frappe.ui.form.on('Delivery Note', 'refresh', function(frm, cdt, cdn){
	var doc = frm.doc

  	if(doc.docstatus ==1){
  		cur_frm.add_custom_button(__('Send Email to Customer'), frm.cscript.send_email_to_customer).addClass('btn-primary')
  	}
})

cur_frm.cscript.send_email_to_customer = function(){
	var doc = cur_frm.doc;
	
	frappe.call({
		freeze: true,
		method:"biggift.biggift.send_email_to_customer.send_deliverynote_link_to_customer",
		args: {dn_id: doc.name, 'customer': doc.customer, 'delivery_note_to': 'Customer'}
	})
}