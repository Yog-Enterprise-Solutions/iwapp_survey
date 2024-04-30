import frappe
import json

@frappe.whitelist()
def get_items(survay_template):
    doc = frappe.get_doc("Survey Template", survay_template)    
    item_list = []
    for item in doc.items:
        item_list.append(item.item_code)
    return item_list
