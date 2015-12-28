frappe.ui.form.on('Sales Order', 'refresh', function(frm, cdt, cdn){
	var doc = frm.doc;
	if(doc.docstatus ==1){
		cur_frm.add_custom_button(__('Make Work Order'), frm.cscript.make_work_order).addClass('btn-primary')
	}
})

cur_frm.cscript.make_work_order = function(){
	frappe.model.open_mapped_doc({
		method: "biggift.biggift.custom_methods.make_work_order",
		frm: cur_frm
	})
}