import frappe
import json
from datetime import datetime,timedelta

@frappe.whitelist()
def create_docs(survey_doc):
    survey_doc = json.loads(survey_doc)
    survey_doctype = frappe.get_doc("Survey",survey_doc['name'])

    items = survey_doc['items']
    serial_numbers= frappe.db.get_list("Serial No", pluck='name')
    warranty_items , non_warranty_items = [], []
    for item in items:
        # frappe.log_error("child items", item)
        if item.get('serial_no') in serial_numbers:
            warranty_items.append(item)
        else:
            non_warranty_items.append(item)

    current_date = datetime.now()
    one_week_from_now = current_date + timedelta(weeks=1)

    doc_refs = {}
    formatted_date = one_week_from_now.strftime("%Y-%m-%d")
    if warranty_items:
        doc = frappe.new_doc("Material Request")
        doc.material_request_type= "Material Issue"    
        for item in warranty_items:
            doc.append("items", {
                "item_code" : item['item'],
                "qty":item['qty'],
                "schedule_date" : formatted_date
                # "uom":item['uom'],                
            })
        doc.insert()
        survey_doctype.material_request = doc.name
        doc_refs["material_request"] =doc.name
    
    if non_warranty_items:
        doc = frappe.new_doc("Opportunity")
        doc.opportunity_from = "Customer"
        doc.party_name = survey_doc['customer']
        doc.custom_surveys_fetched += 1        
        for item in non_warranty_items:
            doc.append("custom_survey_items", {
                "row_id" : item['row_id'],
                "item": item['item'],
                "qty":item['qty'],                
            })
        doc.insert()
        survey_doctype.opportunity_created = doc.name        
        doc_refs["opportunity"] = doc.name
    
    survey_doctype.save()
    return "Successfull"
    
