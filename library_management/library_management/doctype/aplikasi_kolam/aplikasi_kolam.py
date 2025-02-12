# Copyright (c) 2025, zalfa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AplikasiKolam(Document):
	pass
	
	def before_insert(doc):
		doc.reff_stock_entry = '#'
	def on_submit(doc):
		try:
			stock_entry = frappe.get_doc({
				"doctype" : "Stock Entry",
				"stock_entry_type": "Aplikasi Kolam",#Material Issue
				"posting_date" : doc.tanggal,
				"items" : doc.set_item_stock(),
				"company" : doc.company,
				"set_posting_time": 1 
			})
			
			stock_entry.flags.from_custom_app = True
			stock_entry.insert()
			stock_entry.submit()

			total_biaya = stock_entry.total_amount
			siklus = frappe.get_doc("Siklus Tanam", doc.siklus_tanam)
			new_total_biaya = siklus.total_biaya + total_biaya 
			new_hpp_ekor = 0

			try:
				new_hpp_ekor =  new_total_biaya / siklus.jumlah_ikan 
			except Exception as e:
				frappe.throw(f"Proses gagal: {str(e)}")

			siklus.db_set({
				"total_biaya":new_total_biaya,
				"hpp_ikan_ekor":new_hpp_ekor
			})
			
			doc.reff_stock_entry = 	stock_entry.name
			frappe.db.set_value('Aplikasi Kolam', doc.name, 'reff_stock_entry', stock_entry.name)			
		except Exception as e:
			frappe.db.rollback()
			frappe.throw(f"Proses gagal: {str(e)}")

	def before_cancel(self):
		stock_entry = frappe.get_doc("Stock Entry",self.reff_stock_entry)
		try:
			amount = stock_entry.total_amount
			siklus = frappe.get_doc("Siklus Tanam", self.siklus_tanam)
			new_total_biaya = siklus.total_biaya - amount

			stock_entry.flags.from_custom_app = True
			stock_entry.cancel()
			siklus.db_set('total_biaya',new_total_biaya)			 	
		except Exception as e:
			frappe.db.rollback()
			frappe.throw(f"Proses gagal: {str(e)}")


	def set_item_stock(doc):
		kolam = frappe.get_doc("Kolam", doc.kolam) 

		items = []
		for item in doc.item_aplikasi:
			items.append({
				"item_code":item.item_code,
				"qty" : item.quantity,
				"s_warehouse":item.warehouse,
				"cost_center" : kolam.cost_center
			})
		return items