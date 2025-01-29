# Copyright (c) 2025, zalfa and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SiklusTanam(Document):
	pass

	def before_insert(doc):
		doc.total_biaya = '0'