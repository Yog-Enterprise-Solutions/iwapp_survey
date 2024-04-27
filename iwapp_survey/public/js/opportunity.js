frappe.ui.form.on('Opportunity', {
	refresh(frm) {
        
		frm.add_custom_button(__('Create Survey'), function(){
            if (frm.doc.__islocal) {
                frm.save();
            }
            
		// frappe.new_doc("Survey", {
		//     survey_from: "Opportunity", 
		//     customer:frm.doc.party_name, 
        //     from_doctype:frm.doc.name,
		//     contact_person: frm.doc.contact_person,
        //     customer_address:frm.doc.custom_site_address,
		//     assigned_to: frappe.session.user
		// });

        if (frm.doc.__islocal) {
            frm.save();
        }

        frappe.call({
            args: {                
                from_doctype:frm.doc.name,
                customer:frm.doc.party_name,                
                customer_address:frm.doc.custom_site_address,
                assigned_to: frappe.session.user,
                items:frm.doc.items
            },
            method: "iwapp_survey.iwapp_survey.doctype.survey.create_from_opp.create_survey",
            callback: function (response) {
                frappe.msgprint("Survey doctype created");
            }
        });
        

    });
	}
})