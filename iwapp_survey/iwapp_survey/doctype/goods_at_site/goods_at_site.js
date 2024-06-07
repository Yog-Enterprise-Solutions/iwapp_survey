// Copyright (c) 2024, Iwex Informatics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Goods at Site', {
	refresh: function (frm) {
		// Ensure the custom buttons are only added once
		if (!frm.custom_buttons_added) {
			// Add the first button (Return Draft)
			frm.add_custom_button(__("Return Draft"), function () {
				frappe.call({
					method: "iwapp_survey.iwapp_survey.doctype.goods_at_site.goods_at_site.process_return_items",

					args: {
						doc: frm.doc,
						'doc_status': 0
					},
					callback: function (response) {
						if (response.message) {
							frm.set_value('custom_status', 'Returned');
							frappe.msgprint("Successfully created material receipt for return items (Submitted): " + response.message);
							// Add response.message to child table 'Return Item'

							frm.reload_doc();
						}
					}
				});
				// Hide the Return Draft button after click
				frm.remove_custom_button(__("Return Draft"));
			}, __("Create"));

			// Add the second button (Return Submit)
			frm.add_custom_button(__('Return Submit'), function () {

				// frappe.call('ping')
				// .then(r => {
				// 	console.log(r)
				// 	// {message: "pong"}
				// })
				frappe.call({
					method: "iwapp_survey.iwapp_survey.doctype.goods_at_site.goods_at_site.process_return_items",
					args: {
						doc: frm.doc,
						"doc_status": 1
					},
					callback: function (response) {
						if (response.message) {
							frm.set_value('custom_status', 'Completed');

							frappe.msgprint("Successfully created material receipt for return items (Submitted): " + response.message);
							// Add response.message to child table 'Return Item'

							frm.reload_doc();
						}
					}
				});
				// Hide the Return Submit button after click
				frm.remove_custom_button(__('Return Submit'));
			}, __("Create"));

			frm.custom_buttons_added = true;
		}
	}
});