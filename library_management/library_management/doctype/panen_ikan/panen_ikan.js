// Copyright (c) 2025, zalfa and contributors
// For license information, please see license.txt
  
frappe.ui.form.on("Panen Ikan", {
	refresh(frm) {
        if(frm.is_new()){
            frm.set_df_property('customer', 'hidden', true);
            frm.set_df_property('kolam_tujuan', 'hidden', true);
        }

        frm.set_query('kolam_tujuan', function() {
            return {
                filters : {
                    'name' : ['!=', frm.doc.kolam]
                }
            }
        })

        frm.set_query('jenis_ikan', function () {
            return {
                filters : {
                    'item_group' : ['=', 'ikan jual']
                }
            }
        })

        if(frm.doc.jenis_ikan){
            frappe.db.get_value('Item',frm.doc.jenis_ikan,'item_name', (r) => {
                if (r && r.item_name) {
                    nama_ikan =  `<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;margin-top:33px;">${r.item_name}</div>`; 
                    frm.set_df_property("nama_ikan","options",nama_ikan);
                } else {
                    nama_ikan =  `<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;margin-top:33px">nama ikan</div>`;                     
                    frm.set_df_property("nama_ikan","options", nama_ikan); // Kosongkan jika tidak ada deskripsi
                }                
            });
        }else{
            nama_ikan =  `<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;margin-top:33px">nama ikan</div>`;                     
            frm.set_df_property("nama_ikan","options", nama_ikan); // Kosongkan jika tidak ada deskripsi            
        }        
	},

    jenis_transaksi: function(frm){
        frm.set_value('customer',null)
        frm.set_value('kolam_tujuan',null)
        if (frm.doc.jenis_transaksi) {
            if(frm.doc.jenis_transaksi == 'Panen Jual'){
                frm.set_df_property('customer', 'hidden', false);
                frm.set_df_property('customer', 'reqd', true);
                frm.set_df_property('kolam_tujuan', 'hidden', true);
                frm.set_df_property('kolam_tujuan', 'reqd', false);
            }else{
                frm.set_df_property('customer', 'hidden', true);
                frm.set_df_property('customer', 'reqd', false);
                frm.set_df_property('kolam_tujuan', 'reqd', true);                
                frm.set_df_property('kolam_tujuan', 'hidden', false);                
            }
        }else{
            frm.set_df_property('customer', 'hidden', true);
            frm.set_df_property('kolam_tujuan', 'hidden', true);
        }
    },

    kolam:function(frm){
        frm.set_value('kolam_tujuan', null);
        frm.refresh_field('kolam_tujuan');
        frm.set_value('siklus_tujuan',null);
        frm.refresh_field('siklus_tujuan',null);
        fetch_siklus_by_kolam(frm)
        // fetch_siklus_for_kolam(frm,frm.doc.kolam,"siklus_tanam")
        
    },

    kolam_tujuan:function(frm){
        fetch_siklus_for_kolam(frm,frm.doc.kolam_tujuan,"kolam_tujuan","siklus_tujuan")
    },

    jenis_ikan:function(frm){
        if(frm.doc.jenis_ikan){
            frappe.db.get_value('Item',frm.doc.jenis_ikan,'item_name', (r) => {
                if (r && r.item_name) {
                    nama_ikan =  `<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;margin-top:33px;">${r.item_name}</div>`; 
                    frm.set_df_property("nama_ikan","options",nama_ikan);
                } else {
                    nama_ikan =  `<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;margin-top:33px">nama ikan</div>`;                     
                    frm.set_df_property('nama_ikan',"options". nama_ikan); // Kosongkan jika tidak ada deskripsi
                }                
            });
        }else{
            nama_ikan =  `<div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;margin-top:33px;">nama ikan</div>`;                     
            frm.set_df_property('nama_ikan','options', nama_ikan); // Kosongkan jika tidak ada deskripsi
        }
    }

});


function fetch_siklus_by_kolam(frm) {
    if (frm.doc.kolam) {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Siklus Tanam',
                filters: {
                    kolam: frm.doc.kolam,
                    docstatus: 1 
                },
                fields: ['name']
            },
            callback: function(r) {
                if (r.message && r.message.length > 0) {
                    frm.set_value('siklus_tanam', r.message[0].name);
                } else {
                    frappe.msgprint(__('Tidak ada siklus yang sesuai untuk kolam ini.'));
                    frm.set_value("siklus_tanam", null);
                }
            }
        });
    } else {
        frm.set_value('siklus_tanam', null); 
    };        
}

function fetch_siklus_for_kolam(frm,kolam,field_kolam,field_siklus){
    if (frm.doc[field_kolam]) {
        console.log(kolam)
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Siklus Tanam',
                filters: {
                    kolam: kolam,
                    docstatus: 1 
                },
                fields: ['name']
            },
            callback: function(r) {
                if (r.message && r.message.length > 0) {
                    frm.set_value(field_siklus, r.message[0].name);
                } else {
                    frappe.msgprint(__('Tidak ada siklus yang sesuai untuk kolam ini.'));
                    frm.set_value(field_siklus, null);
                }
            }
        });
    } else {
        frm.set_value('siklus_tanam', null); 
    }         
}
