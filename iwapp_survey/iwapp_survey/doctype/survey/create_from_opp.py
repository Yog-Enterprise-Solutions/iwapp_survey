import frappe
import json

@frappe.whitelist()
def create_survey(from_doctype, customer, customer_address, assigned_to, items):
    doc = frappe.new_doc("Survey")
    doc.survey_from = "Opportunity"    
    doc.from_doctype = from_doctype
    doc.customer = customer
    doc.customer_address = customer_address
    doc.assigned_to =  assigned_to
    doc.opportunity_created = from_doctype

    items = json.loads(items)
    for row in items:        
        doc.append("items",{
            "item":row['item_code'],
            "qty":row['qty']
        })        
    doc.insert()
    # doc.save()
    return doc.name