// Copyright (c) 2025, zalfa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Siklus Tanam", {
	refresh(frm) {
        // $('input[data-fieldname="total_biaya"]').css("color","red")    
        // frm.fields_dict['total_biaya'].wrapper.css('background-color', 'lightblue');

        if (frm.doc.kolam) {
            frappe.db.get_value('Kolam', frm.doc.kolam, 'kolam_image_attach', (r) => {
                if (r && r.kolam_image_attach) {
                    frm.set_df_property('kolam_html', 'options', `<img src="${r.kolam_image_attach}" style="max-width:400px; max-height: 300px;">`);
                } else {
                    frm.set_df_property('kolam_html', 'options', 'No image available');
                }
            });        
        } else {
        }         

        const fieldElement = frm.fields_dict['total_biaya'].$wrapper[0]; // Mengakses elemen DOM dari field
        if (fieldElement) {
            const valueElement = fieldElement.querySelector('.control-value.like-disabled-input');
            if (valueElement) {
                valueElement.style.color = 'red';  // Mengubah warna teks menjadi merah
            }
        }
	},

    kolam:function(frm){
        let gbr =``;
        if (frm.doc.kolam) {
            frappe.db.get_value('Kolam', frm.doc.kolam, 'kolam_image_attach', (r) => {
                if (r && r.kolam_image_attach) {
                    gbr =`<img src="${r.kolam_image_attach}" alt="kolam image" width=200" height="200">`;    
                    frm.set_df_property("kolam_html", "options", gbr);        
                } else {

                }
            });
        } else {
            // frm.fields_dict.image_klm.$wrapper.find('img').attr('src', '');
        }     
        
    },

    setup: function (frm) {

        frm.add_fetch('kolam','kolam_name','nama_kolam')
    },

    before_load: function(frm) {
        if (frm.is_new()) {
            frm.set_value('total_biaya', '0');
        }
    }
});
