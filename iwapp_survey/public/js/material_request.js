// frappe.ui.form.on('Material Request', {
//     refresh(frm) {
//         // your code here
//         console.log("triggered mr")
//         if (frm.doc.material_request_type == "Material Issue") {
//             frm.add_custom_button(__('Create Site Survey'), function () {
//                 // 		var doc = frappe.new_doc("Site Survey", {
//                 // 		    from_material_request: frm.doc.name, 
//                 // 		    customer:frm.doc.party_name, 
//                 // 		    contact_person: frm.doc.contact_person,
//                 // 		    assigned_to: frappe.session.user
//                 // 		});
//                 if (frm.doc.__islocal) {
//                     frm.save();
//                 }
//                 frappe.call({
//                     args: {
//                         name: frm.doc.name,
//                         assigned_to: frappe.session.user,
//                         child_table: frm.doc.items
//                     },
//                     method: "iwapp_model.iwapp_model.doctype.site_survey.create_from_mr.create_site_survey"
//                 })
//             }
//             )
//         }

//     },
//     material_request_type(frm){
//         console.log("triggered mr")
//         if (frm.doc.material_request_type == "Material Issue") {
//             frm.add_custom_button(__('Create Site Survey'), function () {
                
//                 if (frm.doc.__islocal) {
//                     frm.save();
//                 }
//                 frappe.call({
//                     args: {
//                         name: frm.doc.name,
//                         assigned_to: frappe.session.user,
//                         child_table: frm.doc.items
//                     },
//                     method: "iwapp_model.iwapp_model.doctype.site_survey.create_from_mr.create_site_survey",
//                     callback: function(r){
//                         frappe.msgprint("Site survey created");
//                         var data = r.message;
//                         console.log(data);
//                     }
//                 })
//             }
//             )
//         }
//         else{
//             frm.remove_custom_button("Create Site Survey")
//         }   
//     }

// })