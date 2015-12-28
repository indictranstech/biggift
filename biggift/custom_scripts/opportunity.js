frappe.ui.form.on('Opportunity', 'refresh', function(frm, cdt, cdn){
  var doc = frm.doc;
    cur_frm.add_custom_button(__('Make Pre Order'), frm.cscript.make_pre_order).addClass("btn-primary");
})

cur_frm.cscript.make_pre_order = function(){
	frappe.model.open_mapped_doc({
		method: "biggift.biggift.custom_methods.make_pre_order",
		frm: cur_frm
	})
}