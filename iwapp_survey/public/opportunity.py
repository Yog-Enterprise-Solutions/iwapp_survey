import frappe

def bs(doc,method=None):
    n = frappe.db.get_list("Survey", filters= {"opportunity_from": doc.name})
    n = len(n)
    doc.custom_number_of_surveys = n