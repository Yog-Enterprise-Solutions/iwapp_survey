import frappe
import json

@frappe.whitelist()
def get_items(project):
    # the list of child tables where project is this..
    # frappe.log_error("projects", f"{type(project)}\n\n{project}")
    projects = json.loads(project)
    # frappe.log_error("projects", f"{projects}")    
    project_list = [item['project_type'] for item in projects]
    
    item_list = frappe.db.get_list("Item") 
    item_list_req=  []
    for item in item_list:
        item_doc = frappe.get_doc("Item", item['name'])
        item_projects = item_doc.custom_project_type
        item_projects = list(map(lambda k: k.project_type, item_projects))

        present = any(project in item_projects for project in project_list)
    #     # frappe.log_error("Projects",f"{projects}\n\n{project_list}")
        if present:            
            item_list_req.append(item['name'])
    # # site_doc.custom_project_type = project
    # # site_doc.save()
    return item_list_req
    
