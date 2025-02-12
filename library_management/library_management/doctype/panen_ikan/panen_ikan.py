# Copyright (c) 2025, zalfa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PanenIkan(Document):
	pass

	def on_submit(doc):
		if doc.jenis_transaksi == "Panen Jual":
			panen_jual(doc)
		else:
			panen_mutasi(doc)
			

def panen_jual(doc):
	try:
		kolam = frappe.get_doc("Kolam",doc.kolam)
		siklus = frappe.get_doc("Siklus Tanam",doc.siklus_tanam )
			
		sales_invoice = frappe.new_doc("Sales Invoice")
		sales_invoice.customer = doc.customer
		sales_invoice.posting_date = doc.tanggal
		sales_invoice.due_date = doc.tanggal
		sales_invoice.company = doc.company
		sales_invoice.set("set_posting_time" , 1)
		sales_invoice.set("items",[])

		sales_invoice.append("items",{
			"item_code" : doc.jenis_ikan,
			"qty"		: doc.quantity,
			"rate"      : doc.harga__ekor,
			"cost_center" : kolam.cost_center
		}) 

		sales_invoice.insert()
		sales_invoice.submit()

		hpp_ikan = siklus.hpp_ikan_ekor * doc.quantity
		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Journal Entry"
		je.posting_date = doc.tanggal
		je.company = doc.company
		je.remark =  f"Jurnal HPP dari Panen Ikan {doc.name}"

		je.append("accounts",{
				"account":"5140.001 - HPP Ikan - BSWD",
				"debit" : hpp_ikan,
				"debit_in_account_currency":hpp_ikan,
				"credit" : 0 ,
				"credit_in_account_currency" : 0,
				"againts" : "1190.001 - WIP Ikan - BSWD"
		})

		je.append("accounts",{
				"account" : "1190.001 - WIP Ikan - BSWD",
				"debit" : 0,
				"debit_in_account_currency":0,
				"credit" : hpp_ikan ,
				"credit_in_account_currency" : hpp_ikan,
				"againt":"5140.001 - HPP Ikan - BSWD",
			})

			# print(je.as_dict())

		je.insert()
		je.submit()

		doc.reff_sales_invoice = sales_invoice.name
		doc.reff_jurnal_hpp    = je.name
		frappe.db.set_value("Panen Ikan",doc.name ,"reff_sales_invoice",sales_invoice.name)		
		frappe.db.set_value("Panen Ikan",doc.name ,"reff_jurnal_hpp",je.name)		
	except Exception as e:
		frappe.throw(f"Proses gagal: {str(e)}")

def panen_mutasi(doc):
	try:
		siklus_asal   = frappe.get_doc("Siklus Tanam",doc.siklus_tanam)
		kolam_asal    = frappe.get_doc("Kolam" , doc.kolam)
		siklus_tujuan = frappe.get_doc("Siklus Tanam",doc.siklus_tujuan )
		kolam_tujuan  = frappe.get_doc("Kolam",doc.kolam_tujuan )

		hpp_ikan = siklus_asal.hpp_ikan_ekor * doc.quantity

		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Journal Entry"
		je.posting_date = doc.tanggal
		je.company = doc.company
		je.remark =  f"Jurnal HPP dari Panen Ikan {doc.name}"

		je.append("accounts",{
				"account":"1190.001 - WIP Ikan - BSWD",
				"debit" : hpp_ikan,
				"debit_in_account_currency":hpp_ikan,
				"credit" : 0 ,
				"credit_in_account_currency" : 0,
				"againts" : "1190.001 - WIP Ikan - BSWD",
				"cost_center" : kolam_tujuan.cost_center	
		})

		je.append("accounts",{
				"account" : "1190.001 - WIP Ikan - BSWD",
				"debit" : 0,
				"debit_in_account_currency":0,
				"credit" : hpp_ikan ,
				"credit_in_account_currency" : hpp_ikan,
				"againt":"1190.001 - WIP Ikan - BSWD",
				"cost_center" : kolam_asal.cost_center
			})

			# print(je.as_dict())

		je.insert()
		je.submit()

		siklus_tujuan.db_set({
			"jenis_bibit_ikan" : doc.jenis_ikan,
			"jumlah_bibit" : siklus_tujuan.jumlah_bibit + doc.quantity,
			"jumlah_ikan"  : siklus_tujuan.jumlah_ikan + doc.quantity,
			"total_biaya"  : siklus_tujuan.total_biaya + hpp_ikan,
			"hpp_ikan_ekor" : (siklus_tujuan.total_biaya + hpp_ikan) / ( siklus_tujuan.jumlah_ikan + doc.quantity) 
		})
		doc.reff_jurnal_hpp    = je.name
		frappe.db.set_value("Panen Ikan",doc.name ,"reff_jurnal_hpp",je.name)		

	except Exception as e:
		frappe.throw (f"Proses gagal: {str(e)}")