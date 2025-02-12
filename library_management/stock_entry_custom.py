import frappe


def validate_stock_entry_source(doc,method):
    if doc.stock_entry_type == "Aplikasi Kolam":
        if not doc.flags.get("from_custom_app"):
            frappe.throw("Stock Entry dengan tipe 'Aplikasi Kolam' hanya boleh dibuat dari Aplikasi Kolam")

    if doc.stock_entry_type == "Tebar Benih":
        if not doc.flags.get("from_custom_app"):
            frappe.throw("Stock Entry dengan tipe 'Tebar Benih' hanya boleh dibuat dari Tebar Benih")

def prevent_cancel(doc,method):
    if doc.stock_entry_type == "Aplikasi Kolam":
        if not doc.flags.get("from_custom_app"):
            frappe.throw("Stock Entry dengan tipe 'Aplikasi Kolam' tidak dapat dibatalkan.")    

    if doc.stock_entry_type == "Tebar Benih":
        if not doc.flags.get("from_custom_app"):
            frappe.throw("Stock Entry dengan tipe 'Tebar Benih' tidak dapat dibatalkan.")    
def tes(doc,method):
    print()