cur_frm.cscript.validate_user = function(){
  var doc = cur_frm.doc;
  frappe.call({
      method: "biggift.biggift.doctype.pre_order.pre_order.validate_user",
      args: {'workflow_state': doc.workflow_state, 'user_roles': user_roles, 'doctype': doc.doctype},
      freeze: true,
      callback: function(r){
      	if(r.message.status == false){
      		cur_frm.disable_save();
      	}else{
          if(doc.latest_comment == 'Unread' && doc.comment_user_name != user){
            cur_frm.set_value('latest_comment', 'Read')
            cur_frm.save()
          }
        }
      } 
  })
}