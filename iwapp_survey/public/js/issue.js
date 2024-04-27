frappe.ui.form.on('Issue', {
    
    refresh: function (frm) {
        // your code here
        console.log("triggered mr")

        frm.add_custom_button(__('Create Survey'), function () {
            // frappe.msgprint("creating Survey")
            // var doc = frappe.new_doc("Survey", {
            //     survey_from: "Issue", 
            //     from_doctype: frm.doc.name,
            //     customer:frm.doc.customer, 
            //     customer_address: frm.doc.custom_site_address,
            //     // project_type:frm.doc.custom_project_type,
            //     assigned_to: frappe.session.user
            // });

            if (frm.doc.__islocal) {
                console.log("saving here.")
                frm.save();
            }

            frappe.call({
                args: {
                    name: frm.doc.name,
                    assigned_to: frappe.session.user,
                    project_type: frm.doc.custom_project_type,
                    customer:frm.doc.customer,
                    site_address:frm.doc.custom_site_address
                },
                method: "iwapp_survey.iwapp_survey.doctype.survey.create_from_issue.create_site_survey",
                callback: function (response) {
                    frappe.msgprint("Survey doctype created");
                },
                async:false
            });
            
        },__("Create")
        )


    },

})