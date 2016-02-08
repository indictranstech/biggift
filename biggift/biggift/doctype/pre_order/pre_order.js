{% include 'custom_scripts/validate_user.js' %}

frappe.ui.form.on('Pre Order', 'refresh', function(frm, cdt, cdn){
  var doc = frm.doc;
  if(doc.docstatus==0 && !doc.__islocal){
    frm.cscript.validate_user()
  }
  
  // if (doc.workflow_state == 'Accepted By Production Team' && in_list(user_roles, 'Manufacturing User')){
  //   cur_frm.add_custom_button(__('Make PO'), frm.cscript.make_purchase_order).addClass("btn-primary");
  // }

  if (doc.workflow_state == 'Accepted' && in_list(user_roles, 'Sales User')){
    cur_frm.add_custom_button(__('Make SAS'), frm.cscript.make_sas).addClass("btn-primary");
  }
})

cur_frm.cscript.make_purchase_order = function(){
  frappe.model.open_mapped_doc({
    method: "biggift.biggift.doctype.pre_order.pre_order.make_purchase_order",
    frm: cur_frm
  })
}


cur_frm.cscript.make_sas = function(){
  frappe.model.open_mapped_doc({
    method: "biggift.biggift.doctype.pre_order.pre_order.make_sas",
    frm: cur_frm
  })
}

cur_frm.fields_dict.sales_person.get_query = function(){
  return {
    query: 'biggift.biggift.doctype.pre_order.pre_order.get_sales_user'
  }
}

cur_frm.add_fetch('customer', 'customer_name', 'customer_name');
cur_frm.add_fetch('lead', 'lead_name', 'customer_name');