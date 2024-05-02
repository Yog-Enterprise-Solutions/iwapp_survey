import frappe
import json

@frappe.whitelist()
def sales_return(doc):
    doc = json.loads(doc)
    dn = frappe.new_doc("Stock Entry") 
    dn.stock_entry_type = "Matarial Receipt"
    # frappe.log_error("ITEMS DATA","\n\n".join(list(map(str,doc['return_items']))))
    for item in doc['return_items']:
        dn.append("items", {
            "item_code": item['item_code'],
            "qty": item['quantity'] * 1,
            "uom":item['uom'],
            "custom_model_id": item['model_id'],
            'serial_no': item['serial_no']
        })
    dn.insert()
    dn.save()
    return "Success"
    
