import frappe
import json

@frappe.whitelist()
def create_site_survey(name,assigned_to,project_type):
    project_type = json.loads(project_type)
    doc = frappe.new_doc("Survey")
    doc.from_doctype = name
    doc.assigned_to =  assigned_to
    frappe.log_error("child table received", f"{type(project_type)}\n\n\n{project_type}")

    for row in project_type:
        pdoc = frappe.new_doc("Project Type ms")
        pdoc.project_type = row['project_type']
        
        doc.append("project_type",pdoc)
        
    doc.insert()
    doc.save()
    return doc.name