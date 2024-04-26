// Copyright (c) 2024, YES and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Survey', {
	refresh: function (frm) {
		frm.add_custom_button("Get Location", function () {
			if (frm.doc.site_location) {
				var url = `https://google.com/maps/@${frm.doc.site_location}`
				window.open(url, '_blank')
			}
		});
		if (frm.doc.from_material_request) {
			frm.add_custom_button("Create Opportunity", function () {
				frappe.call({
					args: {

					}
				})

			})
		}

	},
	custom_project_type: function (frm) {
		// frm.set_value('items', []);
		// frm.refresh_field('items');		
		// frm.set_value("custom_project_type", frm.doc.custom_project_type)
		// if (frm.doc.__islocal){
		// 	frm.save();
		// }
		console.log(frm.doc.custom_project_type)
		frappe.call({
			args: {
				project: frm.doc.custom_project_type,
			},

			method: "iwapp_model.iwapp_model.doctype.site_survey.get_items_from_project.get_items",
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
	}
});
