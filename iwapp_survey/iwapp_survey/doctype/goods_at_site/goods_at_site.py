
import frappe
import json
from frappe.model.document import Document

class GoodsatSite(Document):
    pass

@frappe.whitelist()
def process_return_items():
    data = frappe.form_dict.get('doc')
    if data:
        try:
            data = json.loads(data)
            status = frappe.form_dict.get('doc_status')
            child_table = data.get('return_items', [])
            
            # Create a new "Stock Entry" document
            doc = frappe.new_doc('Stock Entry')
            doc.stock_entry_type = 'Material Receipt'
            doc.docstatus = status

            for item in child_table:
                doc.append("items", {
                    "item_code": item.get('item_code'),
                    "qty": item.get('quantity'),
                    "uom": item.get('uom'),
                    "rate": item.get('rate'),
                    "t_warehouse": 'Stores - C'  # Update with the correct target warehouse if needed
                })

            # Insert the document
            doc.insert()
            frappe.response['message'] = doc.name
        except json.JSONDecodeError:
            frappe.response['message'] = "Error: Invalid JSON data"
    else:
        frappe.response['message'] = "Error: No data received"

# Example usage: 
# Define and populate Goods at Site document
def create_goods_at_site(doc,method=None):
    goods_at_site = frappe.new_doc("Goods at Site")
    goods_at_site.customer = doc.customer
    goods_at_site.delivery_note = doc.name
    goods_at_site.custom_status = "Delivered"


    childtable = doc.items
    for items in childtable:
        goods_at_site.append("custom_delivery_goods_items",{
            "item_code":items.item_code,
            "quantity":items.qty,
            "uom":items.uom,
            "rate":items.rate
        })
    goods_at_site.insert()

# Usage:
# Assuming you have a document object named 'doc'
# create_goods_at_site(doc)



def update_goods_at_site_from_delivery_note(doc,method=None):
    # Get the delivery note name from the first item
    dn = doc.items[0].prevdoc_docname
    
    # Find the related Goods at Site document
    gas_name = frappe.db.get_value("Goods at Site", {"delivery_note": dn}, "name")
    
    # If a related Goods at Site document exists, update it
    if gas_name:
        gs_doc = frappe.get_doc("Goods at Site", gas_name)
        gs_doc.custom_status = "Installed"
       
        # Loop through items in doc and append them to gs_doc
        for item in doc.items:
            gs_doc.append("items", {
                "item_code": item.item_code,
                "quantity": item.qty,
                "uom": "Nos",
                "rate": 0  # Changed from 00 to 0
                # Add more fields as needed
            })

        # Loop through gs_doc items and append them to return_items
        for i in gs_doc.custom_delivery_goods_items:
            gs_doc.append("return_items", {
                "item_code": i.item_code,
                "quantity": i.quantity - item.qty,
                "uom": "Nos",
                "rate": 0  # Changed from 00 to 0
                # Add more fields as needed
            })

        gs_doc.save()
        return True
    else:
        frappe.msgprint("No related Goods at Site document found for the delivery note.")
        return False

# Usage:
# Assuming you have a document object named 'doc'
# update_goods_at_site_from_delivery_note(doc)