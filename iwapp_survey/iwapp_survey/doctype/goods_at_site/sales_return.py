import frappe
import json

@frappe.whitelist()
def sales_return(doc):
    doc = json.loads(doc)
    dn = frappe.new_doc("Delivery Note")
    dn.is_return = 1
    dn.customer = doc['customer']
    frappe.log_error("ITEMS DATA","\n\n".join(list(map(str,doc['return_items']))))
    for item in doc['return_items']:
        dn.append("items", {
            "item_code": item['item_code'],
            "qty": item['quantity'] * -1,
            "uom":item['uom'],
            "rate":item['rate']
        })
    dn.save()
    return "Success"
    
