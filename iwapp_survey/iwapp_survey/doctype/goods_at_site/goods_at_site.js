frappe.ui.form.on('Goods at Site', {
	refresh: function (frm) {
		frm.trigger("update_indicators");

		// Ensure the custom buttons are only added once
		if (!frm.custom_buttons_added) {
			// Add the first button (Return Draft)
			frm.add_custom_button(__("Return Draft"), function () {
				frappe.call({
					method: "iwapp_survey.iwapp_survey.doctype.goods_at_site.goods_at_site.process_return_items",
					args: {
						doc: frm.doc,
						doc_status: 0
					},
					callback: function (response) {
						if (response.message) {
							// Set status and save the form after the status is set
							frm.set_value('status', 'Returned').then(() => {
								return frm.save();
							}).then(() => {
								frappe.msgprint("Successfully created material receipt for return items (Submitted): " + response.message);
							});
						}
					}
				});

				// Hide the Return Draft button after click
				frm.remove_custom_button(__("Return Draft"));
			}, __("Create"));

			// Add the second button (Return Submit)
			frm.add_custom_button(__('Return Submit'), function () {
				frappe.call({
					method: "iwapp_survey.iwapp_survey.doctype.goods_at_site.goods_at_site.process_return_items",
					args: {
						doc: frm.doc,
						doc_status: 1
					},
					callback: function (response) {
						if (response.message) {
							// Set status and save the form after the status is set
							frm.set_value('status', 'Completed').then(() => {
								return frm.save();
							}).then(() => {
								frappe.msgprint("Successfully created material receipt for return items (Submitted): " + response.message);
							});
						}
					}
				});

				// Hide the Return Submit button after click
				frm.remove_custom_button(__('Return Submit'));
			}, __("Create"));

			frm.custom_buttons_added = true;
		}
	},
	update_indicators: function (frm) {
		const status = frm.doc.status;

		switch (status) {
			case "Installed":
				frm.page.set_indicator("Installed", "grey");
				break;
			case "Returned":
				frm.page.set_indicator("Returned", "orange");
				break;
			case "Delivered":
				frm.page.set_indicator("Delivered", "red");
				break;
			case "Completed":
				frm.page.set_indicator("Completed", "blue");
				break;
			default:
				frm.page.clear_indicator();
				break;
		}
	}
});
