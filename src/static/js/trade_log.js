$(document).ready(function() {
    $('#tradesTable').DataTable({
        "order": [[ 12, "desc" ]], // Sort by 'Created Timestamp' column descending
        "paging": true,
        "searching": true,
        "info": true,
        "colReorder": true, // Enable column reordering
        "autoWidth": true // Enable automatic column resizing
    });
});
