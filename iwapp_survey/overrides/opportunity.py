import frappe

def bs(doc,method=None):    
    # frappe.log_error("opp validate", "validate called")
    
    # n = frappe.db.get_list("Survey", or_filters= [["from_doctype" ,"=",  doc.name], ["opportunity_created", '=', doc.name]])
    # n = frappe.db.count("Survey", {'opportunity_created' : doc.name})
    # # n = len(n)    
    # # frappe.throw(f"count : {n}")
    # frappe.throw(f"{doc.name} \n {n}")
    # frappe.db.set_value("Opportunity", doc.name, "custom_number_of_surveys", n)
    # frappe.db.commit()
    pass