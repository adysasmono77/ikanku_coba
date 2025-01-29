# Copyright (c) 2025, zalfa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryTransaction(Document):
	pass

	def before_save(self):
		self.mb1a()

	def mb1a(self):
		
		stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",  # "Material Issue" untuk peminjaman
            "items": self.get_stock_items(),
            "company": self.company,  # Pastikan perusahaan yang sama dengan transaksi
        })
		
		stock_entry.insert()
		stock_entry.submit()

	def get_stock_items(self):
		items = []
		for item in self.item:
			items.append({
				"item_code":item.item_buku,
				"qty" : item.qty,
				"s_warehouse":item.gudang
			})
		return items