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
        $("#job1").jCombo("/register/job/",{
            initial_text:'-- 请选择 --',
        });
        $('#job2').jCombo('/register/job?id=',{
            parent:'#job1',
            initial_text:'-- 请选择 --',
        });
    });

}) (jQuery, window, document);
