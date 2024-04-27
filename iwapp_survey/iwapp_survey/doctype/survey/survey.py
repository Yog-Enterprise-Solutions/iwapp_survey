# Copyright (c) 2024, YES and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Survey(Document):
	def validate(self):
		for i,row in enumerate(self.items):
			row.row_id  = f"{self.name}"

	def on_submit(self):		
		# for i,row in enumerate(self.items):
		# 	row.row_id  = f"{self.name}"
		frappe.log_error("on submit triggered", "submit")
	
		opp_doc = frappe.get_doc("Opportunity", self.from_doctype) 
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
	
	def before_cancel(self):
		document_type = self.survey_from
		if self.opportunity_created or (self.survey_from == "Opportunity" and self.from_doctype):
			ref_name = self.opportunity_created			
			status = frappe.db.get_value("Opportunity", ref_name, "status")
			if status == "Converted":
				frappe.throw(f"Cannot cancel survey when a linked opportunity has been converted")
		
		if self.survey_from == "Opportunity" and self.from_doctype:
			ref_name = self.from_doctype			
			status = frappe.db.get_value("Opportunity", ref_name, "status")
			if status == "Converted":
				frappe.throw(f"Cannot cancel survey when a linked opportunity has been converted")

		elif self.material_request:
			ref_name = self.material_request
			status = frappe.db.get_value("Material Request", ref_name, "status")
			if status == 1:
				frappe.throw("Cannot cancel Survey when Linked Matarial Request is Submitted")
