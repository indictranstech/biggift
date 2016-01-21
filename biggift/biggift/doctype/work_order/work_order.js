frappe.ui.form.on('Work Order Item', 'work_order_attach', function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	refresh_field('wo_image_view', d.name, 'work_order_item')
})

frappe.ui.form.on('Work Order', 'refresh', function(frm, cdt, cdn){
	var doc = frm.doc
	if (doc.docstatus == 1 && in_list(user_roles, 'Sales User') && doc.order_type == 'Sample'){
    	cur_frm.add_custom_button(__('Make Quotation'), frm.cscript.make_quotation).addClass("btn-primary");
  	}
  	if(!doc.__islocal){
  		frm.cscript.make_delivery(frm, cdt, cdn)
  	}

  	if(doc.order_type == 'Sales' && doc.workflow_state == 'QC Accepted'){
  		doc.workflow_state = 'QC Accepted Ready For Dispatch'
  		frm.save()
  	}
})

cur_frm.cscript.make_delivery = function(frm, cdt, cdn){
	var doc = frm.doc;
	var items = doc.work_order_item;
	var msg = true;

	$.each(items, function(k, v){
		if(flt(items[k].delivered_qty) != flt(items[k].qty)){
			msg = false;
		}

		if(msg == false) {return msg}
	})

	if(doc.order_type == 'Sales' && doc.docstatus == 1 && msg == false){
  		cur_frm.add_custom_button(__('Make Delivery Note'), frm.cscript.make_delivery_note).addClass("btn-primary");
  	}
}

cur_frm.cscript.make_quotation = function(frm, cdt, cdn){
	frappe.model.open_mapped_doc({
		method: "biggift.biggift.doctype.work_order.work_order.make_quotation",
		frm: cur_frm
	})
}

cur_frm.cscript.make_delivery_note = function(frm, cdt, cdn){
	frappe.model.open_mapped_doc({
		method: "biggift.biggift.doctype.work_order.work_order.make_delivery_note",
		frm: cur_frm
	})
}	

cur_frm.add_fetch('customer', 'customer_name', 'customer_name');
cur_frm.add_fetch('lead', 'lead_name', 'customer_name');