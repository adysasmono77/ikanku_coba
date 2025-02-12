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
                    frm.set_value('siklus_tanam', "#");
                }
            }
        });
    } else {
        frm.set_value('siklus_tanam', '#'); // Reset jika kolam kosong
    }
};

frappe.custom.get_default_warehouse = function(frm) {
    if(frm.doc.jenis_benih){
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                parent: "Item",
                doctype: "Item Default",
                fields: ["default_warehouse"],
                filters: {
                    parent: frm.doc.jenis_benih // Pastikan jenis_benih adalah Item
                    // parent: frm.doc.jenis_benih
                }
            },
            callback: function(r) {
                if (r.exc) {
                    console.error("Error:", r.exc); // Cetak error detail
                    frm.set_value("gudang", "#"); 
                } else if (r.message.length > 0) {
                    let item_default = r.message[0];
                    console.log("Default Warehouse:", item_default.default_warehouse);
                    if (item_default.default_warehouse == null) {
                        frm.set_value("gudang", "#");                         
                    }else{
                        frm.set_value("gudang", item_default.default_warehouse);
                    }
                } else {
                    frm.set_value("gudang", "#");                                        
                }                

            }
        });

    }else {
        frm.set_value('gudang', '#')
    }
}

frappe.ui.form.on("Tebar Benih", {
	refresh(frm) {
        if (frm.doc.reff_stock_entry) {
            frm.add_custom_button(__('Go to Stock Entry'), function() {
                frappe.set_route('Form', 'Stock Entry', frm.doc.reff_stock_entry);
            });            
        }

	},

    jenis_benih:function(frm){
        if (frm.doc.jenis_benih) {
            frappe.db.get_value('Item', frm.doc.jenis_benih, 'item_name')
                .then((r) => {
                    if (r.message) {
                        frm.set_value('nama_bibit', r.message.item_name);
                    }
                });
        } else {
            frm.set_value('nama_bibit', '#'); // Kosongkan jika item tidak dipilih
        }        

        frappe.custom.get_default_warehouse(frm)
    },

    kolam:function(frm){
        frappe.custom.fetch_siklus_for_kolam(frm)
    },


});


