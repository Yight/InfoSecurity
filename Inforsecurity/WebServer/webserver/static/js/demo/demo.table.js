/*
 * MWS Admin v2.0.2 - Table Demo JS
 * This file is part of MWS Admin, an Admin template build for sale at ThemeForest.
 * All copyright to this file is hold by Mairel Theafila <maimairel@yahoo.com> a.k.a nagaemas on ThemeForest.
 * Last Updated:
 * October 21, 2012
 *
 */

;(function( $, window, document, undefined ) {

    $(document).ready(function() {


        // Data Tables
        if( $.fn.dataTable ) {
            $(".mws-datatable").dataTable();
            $(".mws-datatable-fn").dataTable({
                "iDisplayLength": 10,
                "aLengthMenu": [[10, 20, 30], [10, 20, 30]],
                sPaginationType: "full_numbers",
                "sScrollX": "100%",
                "sScrollXInner": "160%",
                "sDom": '<"top"f>rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_resemails_list/",
                "aoColumns": [
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                ]
            });
        }
        $("<button type='button' class='btn' style='float:right;' id='high_search' href='#inline_content'><i class='icon-search'></i>高级搜索</button>").appendTo('#DataTables_Table_0_filter');

    });

}) (jQuery, window, document);
