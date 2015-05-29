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
        $('.mws-form .mws-form-item>.ui-spinner,.mws-form .mws-form-item>.select2-container,.mws-form .mws-form-item>.fileinput-holder .fileinput-preview').attr('style','width:73%;padding-right: 89px;');

        $('#select_question').change(function(){
            if($('#select_question option:selected').text() == '自己输入问题'){
                $('#custom_question').attr('readonly',false);
            }else{
                $('#custom_question').attr('readonly',true).val('');
            }
        });

        $('#id_captcha_1').attr('style','width:287px;');

        $('.captcha').click(function(){
            $.getJSON('/captcha/refresh/',function(data){
                $('#id_captcha_0').val(data.key);
                $('.captcha').attr('src',data.image_url);
            });
        });
    });


}) (jQuery, window, document);
