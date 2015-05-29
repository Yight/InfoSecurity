/*
 * MWS Admin v2.0.2 - Widgets Demo JS
 * This file is part of MWS Admin, an Admin template build for sale at ThemeForest.
 * All copyright to this file is hold by Mairel Theafila <maimairel@yahoo.com> a.k.a nagaemas on ThemeForest.
 * Last Updated:
 * October 21, 2012
 *
 */

;(function( $, window, document, undefined ) {

    $(document).ready(function() {
    
        //去掉字符串头尾空格   
        function trim(str) {   
            return str.replace(/(^\s*)|(\s*$)/g, "");   
        } 

        if( $.validator ) {
        
            jQuery.validator.addMethod("mobile", function( value, element ) {
            var result = this.optional(element) || /^\d{11}$/.test(value);
            return result;
            }, "Your mobile is invalid.");
            
            jQuery.validator.addMethod("telephone", function( value, element ) {
            var result = this.optional(element) || /^(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/.test(value);
            return result;
            }, "Your telephone is invalid.");
            
            jQuery.validator.addMethod("custom_question", function( value, element ) {
                if($('#select_question').val() == "自己输入问题"){
                    if(value == ""){
                        return false;
                    }
                }
                return true;
            }, "Your custom_question is invalid.");
            $('#register-form').validate({
                    errorPlacement:function(label,elem){
                        elem.closest('.mws-form-row').find('.error-messages').append(label);
                    },
                    rules:{
                        email:{
                            required:true,
                            email:true,
                        },
                        mobile:{
                            required:true,
                            mobile:true,
                        },
                        telephone:{
                            telephone:true,
                        },
                        select_question:{
                            required:true,
                        },
                        custom_question:{
                            custom_question:true,
                        },
                        answer:{
                            required:true,
                        },
                    },
                    messages:{
                        email:{
                            required:"邮箱必须要填",
                            email:"请输入正确的邮箱",
                        },
                        mobile:{
                            required:"手机号码必须要填",
                            mobile:"请输入正确的手机号码",
                        },
                        telephone:{
                            telephone:"请输入正确的电话号码",  
                        },
                        select_question:{
                            required:"密码提示问题必须要填",  
                        },
                        custom_question:{
                            custom_question:"现在你必须输入问题",
                        },
                        answer:{
                            required:"提示问题答案必须要填",  
                        }
                    },
                    invalidHandler: function (form,validator) {
                        var errors = validator.numberOfInvalids();
                        if (errors) {
                            var message = errors == 1 ? '您有一个信息不规范， 请验证' : '您有' + errors + ' 个信息不规范，请验证';
                            $("#mws-validate-error").html(message).show();
                        } else {
                            $("#mws-validate-error").hide();
                        }
                    }
                });
        }
    });
}) (jQuery, window, document);

