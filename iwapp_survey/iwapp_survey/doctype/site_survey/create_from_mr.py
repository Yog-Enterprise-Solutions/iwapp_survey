import frappe
import json

@frappe.whitelist()
def create_site_survey(name,assigned_to,child_table):
    child_table = json.loads(child_table)
    doc = frappe.new_doc("Site Survey")
    doc.from_material_request = name
    doc.assigned_to =  assigned_to
    frappe.log_error("child table received", f"{type(child_table)}\n\n\n{child_table}")
    for row in child_table:
        doc.append("items", {
            "item" : row['item_code'],
            "qty":row['qty']
        })
    doc.insert()
    return doc.name