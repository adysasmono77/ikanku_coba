import frappe

def validate_siklus_kolam(doc, method):
    siklus_doc = frappe.get_doc("Siklus", doc.siklus)
    if siklus_doc.kolam != doc.kolam:
        frappe.throw(
            _("Siklus {0} tidak sesuai dengan Kolam {1}").format(
                doc.siklus, doc.kolam
            )
        )