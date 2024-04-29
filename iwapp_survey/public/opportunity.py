import frappe

def bs(doc,method=None):    
    n = frappe.db.get_list("Survey", or_filters= [["opportunity_from" ,"=",  doc.name], ["opportunity_created", '=', doc.name]])
    n = len(n)
    doc.custom_number_of_surveys = n