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
        doc.save()
        survey_doctype.material_request = doc.name
        doc_refs["material_request"] =doc.name
    
    if non_warranty_items:
        doc = frappe.new_doc("Opportunity")
        doc.opportunity_from = "Customer"
        doc.party_name = survey_doc['customer']
        # doc.custom_survey = survey_doc['name']
        doc.custom_site_address = survey_doc['customer_address']
        doc.custom_surveys_fetched = 1
        doc.custom_number_of_surveys = 1
        for item in non_warranty_items:
            doc.append("custom_survey_items", {
                "row_id" : item['row_id'],
                "item": item['item'],
                "qty":item['qty'],                
            })
            doc.append("items", {
					"item_code":item['item'],
					"qty":item['qty'],
				})
        survey_multiselect = frappe.new_doc("Survey Multiselect")
        survey_multiselect.survey = survey_doc['name']
        
        doc.append("custom_surveys", survey_multiselect)

        doc.insert()
        doc.save()
        survey_doctype.opportunity_created = doc.name        
        doc_refs["opportunity"] = doc.name
    
    survey_doctype.save()
    return "Successfull"

@frappe.whitelist()    
def create_opportunity(survey_doc, items):
    frappe.log_error("items: ", f"{type(items)}\n{items}")
    if items is None:
        frappe.throw("Please select items.")
    survey_doc = json.loads(survey_doc)
    items = json.loads(items)
    survey_doctype = frappe.get_doc("Survey",survey_doc['name'])

    doc = frappe.new_doc("Opportunity")
    doc.opportunity_from = "Customer"
    doc.party_name = survey_doc['customer']
    doc.custom_survey = survey_doc['name']
    doc.custom_site_address = survey_doc['customer_address']
    doc.custom_surveys_fetched = 1
    doc.custom_number_of_surveys = 1
    for item in items:
        # frappe.throw(f"{item} received")
        item_data = frappe.db.get_value("Site Visit Item", item, ["item", "qty", "row_id", "opportunity_created", "material_request_created"])

        if item_data[3] ==1 or item_data[4] == 1 :
            frappe.throw(f"Opportunity already created for item : {item_data[0]}")
        # frappe.throw(f"item here: {item}")
        doc.append("custom_survey_items", {
            "item": item_data[0],            
            "qty":item_data[1],                
            "row_id" : item_data[2],
        })
        doc.append("items", {
                "item_code":item_data[0],
                "qty":item_data[1],
            })
        frappe.db.set_value("Site Visit Item", item, "opportunity_created", 1)

    survey_multiselect = frappe.new_doc("Survey Multiselect")
    survey_multiselect.survey = survey_doc['name']
    
    survey_doctype.opportunity_created = doc.name        
    doc.append("custom_surveys", survey_multiselect)
    doc.insert()
    doc.save()
    
@frappe.whitelist()
def create_mr(survey_doc, items):
    if items is None:
        frappe.throw("Please select items.")
    survey_doc = json.loads(survey_doc)
    items = json.loads(items)

    survey_doctype = frappe.get_doc("Survey",survey_doc['name'])
    

    current_date = datetime.now()
    one_week_from_now = current_date + timedelta(weeks=1)

    formatted_date = one_week_from_now.strftime("%Y-%m-%d")

    doc = frappe.new_doc("Material Request")
    doc.material_request_type= "Material Issue"

    for item in items:        
        item_data = frappe.db.get_value("Site Visit Item", item, ["item", "qty", "row_id", "opportunity_created", "material_request_created"])
        
        if item_data[3] ==1 or item_data[4] == 1:
            frappe.throw(f"Doctype already created for item_data : {item_data[0]}")

        doc.append("items", {
            "item_code" : item_data[0],
            "qty":item_data[1],
            "schedule_date" : formatted_date
            # "uom":item['uom'],                
        })
        frappe.db.set_value("Site Visit Item", item, "material_request_created", 1)
    doc.insert()
    doc.save()
    survey_doctype.material_request = doc.name
