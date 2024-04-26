# Copyright (c) 2024, YES and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SiteSurvey(Document):
	def validate(self):
		for i,row in enumerate(self.items):
			row.row_id  = f"{self.name}"

	def on_submit(self):		
		# for i,row in enumerate(self.items):
		# 	row.row_id  = f"{self.name}"
		opp_doc = frappe.get_doc("Opportunity", self.opportunity_from) 
		new_hash = {}
		for i,row in enumerate(self.items):
			# frappe.log_error("CHild table", f"{row.row_id}")		
			new_hash[row.item] = row.qty	
			opp_doc.append("custom_survey_items", {
				"row_id" : row.row_id,
				"item": row.item,
				"qty":row.qty,
				"uom":row.uom,
				"description": row.description,
				"image1":row.image1,
				"image2":row.image2,
				"image3":row.image3,
				"image4":row.image4,
			})
		for item in opp_doc.items:
			if item.item_code in new_hash:
				item.qty = item.qty + new_hash[item.item_code]
				new_hash[item.item_code] = -1

		for item,qty in new_hash.items():
			frappe.log_error("hash items", f"{item}")
			if qty != -1:
				opp_doc.append("items", {
					"item_code":item,
					"qty":qty,
				})
		opp_doc.save()
		# pass
