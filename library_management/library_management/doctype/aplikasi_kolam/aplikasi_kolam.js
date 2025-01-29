// Copyright (c) 2025, zalfa and contributors
// For license information, please see license.txt

frappe.provide('frappe.custom');
frappe.custom.fetch_siklus_for_kolam = function(frm) {

    if (frm.doc.kolam) {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Siklus Tanam',
                filters: {
                    kolam: frm.doc.kolam,
                    docstatus: 1 // Hanya siklus yang sudah disubmit
                },
                fields: ['name']
            },
            callback: function(r) {
                if (r.message && r.message.length > 0) {
                    frm.set_value('siklus_tanam', r.message[0].name);
                } else {
                    frappe.msgprint(__('Tidak ada siklus yang sesuai untuk kolam ini.'));
                    frm.set_value('siklus_tanam', null);
                }
            }
        });
    } else {
        frm.set_value('siklus_tanam', null); // Reset jika kolam kosong
    }
};



frappe.ui.form.on("Aplikasi Kolam", {
	refresh(frm) {
        if (frm.doc.reff_stock_entry) {
            frm.add_custom_button(__('Go to Stock Entry'), function() {
                frappe.set_route('Form', 'Stock Entry', frm.doc.reff_stock_entry);
            });


            frm.add_custom_button(__('Lihat Account Ledger'), function() {
                let stock_entry_name = frm.doc.reff_stock_entry;
                frappe.route_options = {
					'voucher_no': stock_entry_name
				};
                frappe.set_route('query-report', 'General Ledger', {
                 });

                console.log(frappe) 
            });

        }
	},

    kolam:function(frm){
        frappe.custom.fetch_siklus_for_kolam(frm);
     },

     before_load: function(frm) {
        // if (frm.is_new()) {
        //     frm.set_value('reff_stock_entry', '');
        // }
    }

 });


