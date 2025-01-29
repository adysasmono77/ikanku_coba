# Copyright (c) 2025, zalfa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AplikasiKolam(Document):
	pass
	
	def before_insert(doc):
		doc.reff_stock_entry = '#'
	def on_submit(doc):
		# frappe.msgprint('hello wolrd')
		try:
			# frappe.db.begin()
			stock_entry = frappe.get_doc({
				"doctype" : "Stock Entry",
				 "stock_entry_type": "Aplikasi Kolam",#Material Issue
				"items" : doc.set_item_stock(),
				"company" : doc.company
			})
			
			stock_entry.insert()
			stock_entry.submit()

			total_biaya = stock_entry.total_amount
			siklus = frappe.get_doc("Siklus Tanam", doc.siklus_tanam)
			new_total_biaya = siklus.total_biaya + total_biaya 
			siklus.db_set('total_biaya',new_total_biaya)
			
			doc.reff_stock_entry = 	stock_entry.name
			frappe.db.set_value('Aplikasi Kolam', doc.name, 'reff_stock_entry', stock_entry.name)			
		except Exception as e:
			frappe.db.rollback()
			frappe.throw(f"Proses gagal: {str(e)}")

	# def before_save(doc):


	def set_item_stock(doc):
		items = []
		for item in doc.item_aplikasi:
			items.append({
				"item_code":item.item_code,
				"qty" : item.quantity,
				"s_warehouse":item.warehouse
			})
		return items