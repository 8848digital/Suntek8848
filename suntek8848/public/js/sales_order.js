frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        frm.dashboard.clear_headline();

        if (frm.doc.project) {
            let project_name = frm.doc.project;
            let url = `/app/delivery-request?custom_project=${encodeURIComponent(project_name)}`;

            frappe.call({
                method: "frappe.client.get_count",
                args: {
                    doctype: "Delivery Request",
                    filters: { custom_project: project_name }
                },
                callback: function(response) {
                    let count = response.message || 0;
                    
                    let html = `
                        <h4>Linked Delivery Requests</h4>
                        <div class='document-link-badge'><a href="${url}" target="_blank">
                            Delivery Request (${count})
                        </a></div>
                    `;
                    frm.dashboard.add_section(html);
                }
            });
        } else {
            frm.dashboard.add_section("<p>No Project Linked. Cannot filter Delivery Requests.</p>");
        }
    }
});