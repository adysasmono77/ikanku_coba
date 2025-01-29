// Copyright (c) 2025, zalfa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Membership", {
	// refresh(frm) {
    //     alert('hiii')
	// },

    setup: function (frm) {
        frm.add_fetch('membership','full_name','full_name')    
    },

    // membership: function(frm){
    //     // alert('hii');
    //     if (frm.doc.membership) {
    //         // alert('halo')
    //         frm.set_value('full_name','tesss')
    //     } else {
    //         // alert('deleted')
    //         frm.set_value('full_name','')
    //     }
    // }
});
