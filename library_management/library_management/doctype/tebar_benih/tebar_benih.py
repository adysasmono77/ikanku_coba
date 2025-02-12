# Copyright (c) 2025, zalfa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TebarBenih(Document):
	pass

	def before_insert(doc):
		doc.reff_stock_entry = '#'

	def on_submit(doc):
		try:
			siklus = frappe.get_doc("Siklus Tanam", doc.siklus_tanam)

			stock_entry = frappe.get_doc({
				"doctype" : "Stock Entry",
				"stock_entry_type" : "Tebar Benih",
				"posting_date" : doc.tanggal,
				"items" : doc.set_item_stock(),
				"company" : doc.company,
				"set_posting_time" : 1
			})

			stock_entry.flags.from_custom_app = True
			stock_entry.insert()
			stock_entry.submit()

			total_biaya = stock_entry.total_amount

			new_total_biaya = siklus.total_biaya + total_biaya 
			hpp_ekor = 0
			try:
				hpp_ekor = siklus.total_biaya /  doc.quantity + siklus.jumlah_ikan  
			except Exception as e:
				print()
			siklus.db_set({
				'total_biaya':new_total_biaya,
				'jenis_bibit_ikan': doc.jenis_benih,
				'nama_bibit' : doc.nama_bibit,
				'jumlah_bibit' : doc.quantity + siklus.jumlah_bibit,
				'jumlah_ikan' : doc.quantity + siklus.jumlah_ikan,
				'hpp_ikan_ekor' : hpp_ekor
			})
				
			doc.reff_stock_entry = 	stock_entry.name

		except Exception as e:
			frappe.db.rollback()
			frappe.throw(f"Proses gagal : {str(e)}")

	def set_item_stock(doc):
		kolam = frappe.get_doc("Kolam", doc.kolam) 
		items = []
		items.append({
			"item_code" : doc.jenis_benih,
			"s_warehouse" : doc.gudang,
			"qty" : doc.quantity,
			"cost_center" : kolam.cost_center
		})

		return items