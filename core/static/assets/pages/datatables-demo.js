/*
 Template Name: Ubazo - Admin & Dashboard Template
 Author: Myra Studio
 File: Datatables
*/


$(document).ready(function() {

    // Default Datatable
    $('#vendor-datatable').DataTable({
            "paging": false,
            "info": false,
            "select":true  ,
            "scrollY":"200px",
            "dom": 'Pfrtip',
            ajax: '/vendor/',      
            "columns": [
                { data: 'vendor' },
                { data: 'Name_1' },
                { data: 'City' },
                { data: 'Postal_Code' },
                { data: 'Region' },
                { data: 'Street' },
                { data: 'Email' },           
            ]     
    });
    var table = $('#vendor-datatable').DataTable();
     
    $('#vendor-datatable tbody').on('click', 'tr', function () {
        var d = table.row( this ).row().data();
        alert( d );
        console.log(d);
    } );
    //Buttons examples
    var table = $('#invoice-datatable').DataTable({
        lengthChange: false,
        striped:true,
        ajax: '/invoice/',      
            "columns": [
                { data: 'company_code' },
                { data: 'vendor' },
                { data: 'clearing_date' },
                { data: 'clearing_document' },
                { data: 'assignment' },
                { data: 'fiscal_year' },
                { data: 'document_number' },           
            ],     
        buttons: ['copy', 'csv', 'pdf'],
        "language": {
            "paginate": {
                "previous": "<i class='mdi mdi-chevron-left'>",
                "next": "<i class='mdi mdi-chevron-right'>"
            }
        },
        "drawCallback": function () {
            $('.dataTables_paginate > .pagination').addClass('pagination-rounded');
        }
    });

});

