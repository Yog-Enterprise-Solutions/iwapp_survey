// Copyright (c) 2024, Iwex Informatics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Goods at Site', {
	refresh: function(frm) {
		frm.add_custom_button(__("Return"), function() {
			frappe.call({
				args: {doc:frm.doc},
				method: "iwapp_model.iwapp_model.doctype.goods_at_site.sales_return.sales_return",
				callback: function (r){
					console.log(r);
					frappe.msgprint("Successfully created delivery note for return items")
				}
			})			
		})
	}
});
