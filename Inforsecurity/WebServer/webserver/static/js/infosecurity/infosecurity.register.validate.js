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

        /**  
         * 身份证15位编码规则：dddddd yymmdd xx p   
         * dddddd：地区码   
         * yymmdd: 出生年月日   
         * xx: 顺序类编码，无法确定   
         * p: 性别，奇数为男，偶数为女  
         * <p />  
         * 身份证18位编码规则：dddddd yyyymmdd xxx y   
         * dddddd：地区码   
         * yyyymmdd: 出生年月日   
         * xxx:顺序类编码，无法确定，奇数为男，偶数为女   
         * y: 校验码，该位数值可通过前17位计算获得  
         * <p />  
         * 18位号码加权因子为(从右到左) Wi = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2,1 ]  
         * 验证位 Y = [ 1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2 ]   
         * 校验位计算公式：Y_P = mod( ∑(Ai×Wi),11 )   
         * i为身份证号码从右往左数的 2...18 位; Y_P为脚丫校验码所在校验码数组位置  
         *   
         */  
          
        var Wi = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1 ];// 加权因子   
        var ValideCode = [ 1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2 ];// 身份证验证位值.10代表X   
        function IdCardValidate(idCard) {   
            idCard = trim(idCard.replace(/ /g, ""));   
            if (idCard.length == 15) {   
                return isValidityBrithBy15IdCard(idCard);   
            } else if (idCard.length == 18) {   
                var a_idCard = idCard.split("");// 得到身份证数组   
                if(isValidityBrithBy18IdCard(idCard)&&isTrueValidateCodeBy18IdCard(a_idCard)){   
                    return true;   
                }else {   
                    return false;   
                }   
            } else {   
                return false;   
            }   
        }   
        /**  
         * 判断身份证号码为18位时最后的验证位是否正确  
         * @param a_idCard 身份证号码数组  
         * @return  
         */  
        function isTrueValidateCodeBy18IdCard(a_idCard) {   
            var sum = 0; // 声明加权求和变量   
            if (a_idCard[17].toLowerCase() == 'x') {   
                a_idCard[17] = 10;// 将最后位为x的验证码替换为10方便后续操作   
            }   
            for ( var i = 0; i < 17; i++) {   
                sum += Wi[i] * a_idCard[i];// 加权求和   
            }   
            valCodePosition = sum % 11;// 得到验证码所位置   
            if (a_idCard[17] == ValideCode[valCodePosition]) {   
                return true;   
            } else {   
                return false;   
            }   
        }   
        /**  
         * 通过身份证判断是男是女  
         * @param idCard 15/18位身份证号码   
         * @return 'female'-女、'male'-男  
         */  
        function maleOrFemalByIdCard(idCard){   
            idCard = trim(idCard.replace(/ /g, ""));// 对身份证号码做处理。包括字符间有空格。   
            if(idCard.length==15){   
                if(idCard.substring(14,15)%2==0){   
                    return 'female';   
                }else{   
                    return 'male';   
                }   
            }else if(idCard.length ==18){   
                if(idCard.substring(14,17)%2==0){   
                    return 'female';   
                }else{   
                    return 'male';   
                }   
            }else{   
                return null;   
            }   
        }   
         /**  
          * 验证18位数身份证号码中的生日是否是有效生日  
          * @param idCard 18位书身份证字符串  
          * @return  
          */  
        function isValidityBrithBy18IdCard(idCard18){   
            var year =  idCard18.substring(6,10);   
            var month = idCard18.substring(10,12);   
            var day = idCard18.substring(12,14);   
            var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));   
            // 这里用getFullYear()获取年份，避免千年虫问题   
            if(temp_date.getFullYear()!=parseFloat(year)   
                  ||temp_date.getMonth()!=parseFloat(month)-1   
                  ||temp_date.getDate()!=parseFloat(day)){   
                    return false;   
            }else{   
                return true;   
            }   
        }   
          /**  
           * 验证15位数身份证号码中的生日是否是有效生日  
           * @param idCard15 15位书身份证字符串  
           * @return  
           */  
          function isValidityBrithBy15IdCard(idCard15){   
              var year =  idCard15.substring(6,8);   
              var month = idCard15.substring(8,10);   
              var day = idCard15.substring(10,12);   
              var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));   
              // 对于老身份证中的你年龄则不需考虑千年虫问题而使用getYear()方法   
              if(temp_date.getYear()!=parseFloat(year)   
                      ||temp_date.getMonth()!=parseFloat(month)-1   
                      ||temp_date.getDate()!=parseFloat(day)){   
                        return false;   
                }else{   
                    return true;   
                }   
          }   
        //去掉字符串头尾空格   
        function trim(str) {   
            return str.replace(/(^\s*)|(\s*$)/g, "");   
        } 

        if( $.validator ) {
            jQuery.validator.addMethod("ip", function( value, element ) {
		        var result = this.optional(element) || /^\d{1,3}(?:\.\d{1,3}){3}$/.test(value);

		        if (!result) {
			        var validator = this;
			        //setTimeout(function() {
				        //validator.blockFocusCleanup = true;
				       // element.focus();
				        //validator.blockFocusCleanup = false;
			        //}, 1);
		        }
		        return result;
	        }, "Your ip is invalid.");

            jQuery.validator.addMethod("username", function( value, element ) {
		        var result = this.optional(element) || /^[a-zA-Z]{1}[\w_]+?$/.test(value);

		        return result;
	        }, "Your username is invalid.");

            jQuery.validator.addMethod("password", function( value, element ) {
		        var result = this.optional(element) || /^[\w]+?$/.test(value);

		        return result;
	        }, "Your password is invalid.");
            
            jQuery.validator.addMethod("realname", function( value, element ) {
		        var result = this.optional(element) || /^[\u4e00-\u9fa5]{2,4}$/.test(value);

		        return result;
	        }, "Your realname is invalid.");
            
            jQuery.validator.addMethod("idnum", function( value, element ) {
		        var result = this.optional(element) || IdCardValidate(value);

		        return result;
	        }, "Your idnum is invalid.");
            
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
                    username:{
                        required:true,
                        minlength:6,
                        maxlength:16,
                        username:true,
                    },
                    password:{
                        required:true,
                        minlength:8,
                        maxlength:16,
                        password:true,
                    },
                    repassword:{
                        required:true,
                        equalTo:'#password',
                    },
                    realname:{
                        required:true,
                        realname:true, 
                    },
                    idnum:{
                        required:true,
                        idnum:true,
                    },
                    idpic:{
                        required:true,
                        accept:"jpeg|gif|png|bmp|jpg",
                    },
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
                    job1:{
                        required:true,
                    },
                    job2:{
                        required:true,
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
                    captcha_1:{
                        required:true,
                        remote:{
                            url:'/captcha/verify/',
                            type:'get',
                            dataType:'json',
                            data:{
                                verify_data:function(){
                                        return $('#id_captcha_1').val();
                                    },
                                key:function(){
                                        return $('#id_captcha_0').val();
                                    },
                            },
                        }
                    },
                },
                messages:{
                    username:{
                        required:"用户名必须要填(字母数字下划线组成，6到16位，且第一位必须为字母)",
                        minlength:"用户名至少为6位",
                        maxlength:"用户名至多为16位",
                        username:'用户名由字母数字下划线组成，6到16位，且第一位必须为字母',
                    },
                    password:{
                        required:"密码必须要填(由字母数字下划线组成的字符串，最少为8位)", 
                        minlength:"密码至少为8位",
                        maxlength:"密码至多为16位",
                        password:"密码由字母数字下划线组成的字符串，最少为8位",
                    },
                    repassword:{
                        required:'重复密码必须要填',  
                        equalTo:'此处必须输入和上栏密码相同的内容',
                    },
                    realname:{
                        required:"真实姓名必须要填（2-4个汉字）",
                        realname:'真实姓名必须是2-4个汉字',
                    },
                    idnum:{
                        required:"身份证号必须要填",
                        idnum:'请输入正确的身份证号',
                    },
                    idpic:{
                        required:"身份证号照片必须要有",
                        accept:'请选择正确的身份证号照片',
                    },
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
                    job1:{
                        required:"职业必须要填",
                    },
                    job2:{
                        required:"职业必须要填",
                    },
                    select_question:{
                        required:"密码提示问题必须要填",  
                    },
                    custom_question:{
                        custom_question:"现在你必须输入问题",
                    },
                    answer:{
                        required:"提示问题答案必须要填",  
                    },
                    captcha_1:{
                        required:"验证码必须要填",  
                        remote:"输入验证码错误",
                    },
                },
            });

            $("#mws-validate").validate({
                rules: {
                    sip: {
                        ip: true,
                    },
                    dip: {
                        ip: true,
                    },
                    sender: {
                        email:true,    
                    },
                    receiver :{
                        email:true,
                    },
                    riskvalue: {
                        digits:true,
                    },
                },
                messages:{
                    sip:{
                        ip:"请输入正确格式的ip地址."
                    },
                    dip:{
                        ip:"请输入正确格式的ip地址."
                    },
                    sender:{
                        email:"请输入正确格式的地址."
                    },
                    receiver:{
                        email:"请输入正确格式的地址."
                    },
                    riskvalue:{
                        digits:"请输入正确格式的风险值."
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#mws-validate-error").html(message).show();
                    } else {
                        $("#mws-validate-error").hide();
                    }
                }
            });

            $('#mws-validate').submit(function(eventdata,event){

                if(!($('#begintime').val()||$('#endtime').val()||$('#sip').val()||$('#dip').val()||$('#sender').val()||$('#receiver').val()||$('#riskvalue').val()||$('#resemailtype0').attr('checked')||$('#resemailtype1').attr('checked')||$('#resemailtype2').attr('checked'))){
                    var message = 'You should select least one.';
                    $("#mws-validate-error").html(message).show();
                    event.preventDefault();
                }
                if((new Date($('#begintime').val())) > (new Date($('#endtime').val()))){
                    var message = 'You should make your begintime less your endtime';
                    $("#mws-validate-error").html(message).show();
                    event.preventDefault();
                }
            });
        }
    });
}) (jQuery, window, document);

