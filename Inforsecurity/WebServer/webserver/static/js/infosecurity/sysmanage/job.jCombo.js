/*
 * MWS Admin v2.0.2 - Table Demo JS
 * This file is part of MWS Admin, an Admin template build for sale at ThemeForest.
 * All copyright to this file is hold by Mairel Theafila <maimairel@yahoo.com> a.k.a nagaemas on ThemeForest.
 * Last Updated:
 * October 21, 2012
 *
 */
//job选择列表控件的初始化
;(function( $, window, document, undefined ) {

    $(document).ready(function() {
        $("#add_sub_category_top").jCombo("/register/job/",{
            initial_text:'请选择',
        });
        $("#delete_top_category").jCombo("/register/job/",{
            initial_text:'请选择',
        });
        $("#delete_sub_category_top").jCombo("/register/job/",{
            initial_text:'请选择',
        });
        $('#delete_sub_category').jCombo('/register/job?id=',{
            parent:'#delete_sub_category_top',
            initial_text:'请选择',
        });
    });

}) (jQuery, window, document);
