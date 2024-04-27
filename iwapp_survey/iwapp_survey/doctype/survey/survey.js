// Copyright (c) 2024, YES and contributors
// For license information, please see license.txt

frappe.ui.form.on('Survey', {	
	setup: function(frm){
        frm.set_indicator_formatter('item',
            function(doc) {
                console.log(doc)
				var status = "orange";
				if (doc.serial_no)
				{
					console.log("serial no found", doc.serial_no);
					frappe.call({
						args: {
							doctype:"Serial No",							
							serial_no:doc.serial_no
						},
						method:"frappe.client.get_list",
						callback: function(r){
							// console.log("serial no doctype data");
							// console.log(r.message);
							for (let data of r.message){
								if (data.name == doc.serial_no){
									status = "green";
									doc.warranty_status = 1;
									console.log("serial no found...", doc.serial_no,status)																		
									
								}
								else{
									console.log("not found", doc.serial_no, data.name)
								}
							}
						},
						async: false
					})
				}		
				console.log(doc.serial_no,status)
                return status

            })
    },
	refresh: function (frm) {
		frm.set_query("survey_from", function(){
			return {
				// "filters": {
				// 	"name": "Material Request"
				// }
				"filters": [
					["name" ,"IN", "Opportunity, Issue"],
				]
			}
		});
		
		frm.add_custom_button("Get Location", function () {
			if (frm.doc.site_location) {
				var url = `https://google.com/maps/@${frm.doc.site_location}`
				window.open(url, '_blank')
			}
		});
		frm.add_custom_button("Create Opportunity and M.R", function () {
			frappe.call({
				args: {
					survey_doc: frm.doc
				},
				method: "iwapp_survey.iwapp_survey.doctype.survey.create_opportunity_mr.create_docs",
				callback: function(r){
					frappe.msgprint("Doctypes created");
					var data = r.message;
					console.log(data);
					if (data.material_request){
						frm.doc.material_request = data.material_request;
					}
					if (data.opportunity){
						frm.doc.opportunity_created = data.opportunity;
					}
					frm.refresh_fields();
					frm.save();
				}

			})
		});
		

	},
	survey_from:function(frm){
		if (frm.doc.survey_from == "Issue"){
			frm.set_df_property("from_doctype", 'label', "Issue");
		}
		else{
			frm.set_df_property("from_doctype", 'label', "Opportunity");
		}
	},
	onload:function(frm){
		frm.set_query("opportunity_from", function(){
			return {
				"filters": {
					"name": "Material Request"
				}
			}
		});
	},
	project_type: function (frm) {
		// frm.set_value('items', []);
		// frm.refresh_field('items');		
		// frm.set_value("custom_project_type", frm.doc.custom_project_type)
		// if (frm.doc.__islocal){
		// 	frm.save();
		// }
		console.log(frm.doc.custom_project_type)
		frappe.call({
			args: {
				project: frm.doc.project_type,
			},

			method: "iwapp_survey.iwapp_survey.doctype.survey.get_items_from_project.get_items",
			callback: function (r) {
				// frappe.msgprint("items added successfully");
				// frm.reload_doc();

				console.log(r.message);
				frm.set_value("items", []);
				frappe.model.clear_table(frm.doc, 'items');
				for (var item of r.message) {
					// console.log(item);
					var childTable = frm.add_child("items");
					childTable.item = item;
					childTable.qty = 1;

				}
				
					// frm.reload_doc();
				frm.refresh_fields("items");
				

			}
		})

	},
	onload(frm) {
		if (frm.doc.from_material_request) {
			frm.add_custom_button("Create Opportunity", function () {
				// frappe.call({
				// 	args: {

				// 	}
				// })
			})
		}
	},
	create: function(frm){
		frappe.msgprint("button click working here")
	}
	// customer: function(frm){
	// 	frm.set_query("customer_address", function(){
	// 		return {
	// 			// "filters": {
	// 			// 	"name": "Material Request"
	// 			// }
	// 			"filters": [
	// 				["name" ,"IN", "Opportunity, Material Request"],
	// 			]
	// 		}
	// 	});
	// }
});
