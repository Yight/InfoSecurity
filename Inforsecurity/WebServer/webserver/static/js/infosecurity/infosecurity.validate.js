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
                        var message = errors == 1 ? 'You had one error. It has been highlighted' :'You had' + errors + ' errors. They have been highlighted';
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
            
    /******************************url-search-validate***********************/
            $("#url-search-validate").validate({
                rules: {
                    sip: {
                        ip: true,
                    },
                    dip: {
                        ip: true,
                    },
                    url :{
                        url:true,
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
                    url:{
                        url:"请输入正确格式的url."
                    },
                    riskvalue:{
                        digits:"请输入正确格式的风险值."
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#url-search-validate-error").html(message).show();
                    } else {
                        $("#url-search-validate-error").hide();
                    }
                }
            });

            $('#url-search-validate').submit(function(eventdata,event){

                if(!($('#begintime').val()||$('#endtime').val()||$('#sip').val()||$('#dip').val()||$('#url').val()||$('#riskvalue').val()||$('#resurltype0').attr('checked')||$('#resurltype1').attr('checked')||$('#resurltype2').attr('checked'))){
                    var message = 'You should select least one.';
                    $("#url-search-validate-error").html(message).show();
                    event.preventDefault();
                }
                if((new Date($('#begintime').val())) > (new Date($('#endtime').val()))){
                    var message = 'You should make your begintime less your endtime';
                    $("#url-search-validate-error").html(message).show();
                    event.preventDefault();
                }
            });

            
/******************************url-search-validate***********************/
            $("#url-search-validate").validate({
                rules: {
                    sip: {
                        ip: true,
                    },
                    dip: {
                        ip: true,
                    },
                    ip :{
                        ip:true,
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
                    ip:{
                        ip:"请输入正确格式的ip."
                    },
                    riskvalue:{
                        digits:"请输入正确格式的风险值."
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#ip-search-validate-error").html(message).show();
                    } else {
                        $("#ip-search-validate-error").hide();
                    }
                }
            });

            $('#ip-search-validate').submit(function(eventdata,event){

                if(!($('#begintime').val()||$('#endtime').val()||$('#sip').val()||$('#dip').val()||$('#ip').val()||$('#riskvalue').val()||$('#resiptype0').attr('checked')||$('#resiptype1').attr('checked')||$('#resiptype2').attr('checked'))){
                    var message = 'You should select least one.';
                    $("#ip-search-validate-error").html(message).show();
                    event.preventDefault();
                }
                if((new Date($('#begintime').val())) > (new Date($('#endtime').val()))){
                    var message = 'You should make your begintime less your endtime';
                    $("#ip-search-validate-error").html(message).show();
                    event.preventDefault();
                }
            });
            
/******************************white_ip_add*******************************/
            $("#white_ip_add").validate({
                rules: {
                    white_ip: {//这里每一项对应一项name
                        required:true,
                        ip:true,
                    },
                },
                messages:{
                    white_ip: {
                        required:"请输入正确格式的IP",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();
                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-white_ip-error").html(message).show();
                    } else {
                        $("#add-white_ip-error").hide();
                    }
                }
            });
/******************************white_url_add*******************************/
            $("#white_url_add").validate({
                rules: {
                    white_url: {//这里每一项对应一项name
                        required:true,
                        url:true,
                    },
                },
                messages:{
                    white_url: {
                        required:"请输入URL",
                        url:"请输入正确格式的URL"
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-white_url-error").html(message).show();
                    } else {
                        $("#add-white_url-error").hide();
                    }
                }
            });
/******************************white_email_add*******************************/
            $("#white_email_add").validate({
                rules: {
                    white_email: {//这里每一项对应一项name
                        required:true,
                        email:true,
                    },
                },
                messages:{
                    white_email: {
                        required:"请输入正确格式的email",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-white_email-error").html(message).show();
                    } else {
                        $("#add-white_email-error").hide();
                    }
                }
            });

/******************************whiteProcess_add*******************************/
            
            $("#whiteProcess_add").validate({
                rules: {
                    //这里每一项对应一项name
                    processname: {
                        required:true,
                    },
                    md5: {
                        required:true,
                    },
                },
                messages:{
                    processname: {
                        required:"请输入进程名称",
                    },
                    md5:{
                        required:"请输入MD5",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-whiteProcess-error").html(message).show();
                    } else {
                        $("#add-whiteProcess-error").hide();
                    }
                }
            });

/******************************whiteProcess_edit*******************************/
            $("#whiteProcess_edit").validate({
                rules: {
                    processname: {
                        required:true,
                    },
                    md5: {
                        required:true,
                    },
                },
                messages:{
                    processname: {
                        required:"请输入进程名称",
                    },
                    md5:{
                        required:"请输入MD5",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#edit-whiteProcess-error").html(message).show();
                    } else {
                        $("#edit-whiteProcess-error").hide();
                    }
                }
            });

            $('#whiteProcess_search').submit(function(eventdata,event){

                if(!($('#endtime').val()||$('#begintime').val()||$('#processname').val()||$('#md5').val()||$('#version').val())){
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

    /******************************blackemail_high_search***********************/
            $("#blackemail_search").validate({
                rules: {
                    blackemail: {
                        email:true,
                    },
                    riskvalue: {
                        digits:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackemail:{
                        email:"请输入正确格式的地址."
                    },
                    riskvalue:{
                        digits:"请输入正确格式的风险值.",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
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

    /******************************blackemail_add*******************************/
            $("#blackemail_add").validate({
                rules: {
                    blackemailtype: {//这里每一项对应一项name
                        required:true,
                    },
                    blackemail: {
                        email:true,
                        required:true,
                    },
                    riskvalue: {
                        digits:true,
                        required:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackemailtype: {
                        required:"请选择邮件类型",
                    },
                    blackemail:{
                        required:"请输入邮件地址",
                        email:"请输入正确格式的地址.",
                    },
                    riskvalue:{
                        required:"请输入风险值",
                        digits:"请输入数字",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-blackemail-error").html(message).show();
                    } else {
                        $("#add-blackemail-error").hide();
                    }
                }
            });
/******************************blackemail_edit*******************************/
            $("#blackemail_edit").validate({
                rules: {
                    blackemailtype: {//这里每一项对应一项name
                        required:true,
                    },
                    blackemail: {
                        email:true,
                        required:true,
                    },
                    riskvalue: {
                        digits:true,
                        required:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackemailtype: {
                        required:"请选择邮件类型",
                    },
                    blackemail:{
                        required:"请输入邮件地址",
                        email:"请输入正确格式的地址.",
                    },
                    riskvalue:{
                        required:"请输入风险值",
                        digits:"请输入数字",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#edit-blackemail-error").html(message).show();
                    } else {
                        $("#edit-blackemail-error").hide();
                    }
                }
            });

            $('#blackemail_search').submit(function(eventdata,event){

                if(!($('#endtime').val()||$('#begintime').val()||$('#blackemail').val()||$('#riskvalue').val()||$('#blackemailtype0').attr('checked')||$('#blackemailtype1').attr('checked'))){
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
            
/******************************blackip_custom_validate***********************/
            jQuery.validator.addMethod("ip", function(value, element) { 
            var ip = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/; 
            return this.optional(element) || (ip.test(value) && (RegExp.$1 < 256 && RegExp.$2 < 256 && RegExp.$3 < 256 && RegExp.$4 < 256)); 
            }, "IP地址格式错误"); 
/******************************blackurl_high_search***********************/
            $("#blackurl_search").validate({
                rules: {
                    blackIp: {
                        ip:true,
                    },
                    riskvalue: {
                        digits:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackIp:{
                        ip:"请输入正确格式的地址."
                    },
                    riskvalue:{
                        digits:"请输入正确格式的风险值.",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
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
/******************************blackIp_add*******************************/
            
            $("#blackIp_add").validate({
                rules: {
                    blackiptype: {//这里每一项对应一项name
                        required:true,
                    },
                    blackip: {
                        ip:true,
                        required:true,
                    },
                    riskvalue: {
                        digits:true,
                        required:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackiptype: {
                        required:"请选择IP类型",
                    },
                    blackip:{
                        required:"请输入IP地址",
                        ip:"请输入正确格式的地址.",
                    },
                    riskvalue:{
                        required:"请输入风险值",
                        digits:"请输入数字",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-blackIp-error").html(message).show();
                    } else {
                        $("#add-blackIp-error").hide();
                    }
                }
            });
/******************************blackIp_edit*******************************/
            $("#blackIp_edit").validate({
                rules: {
                    blackiptype: {//这里每一项对应一项name
                        required:true,
                    },
                    blackip: {
                        ip:true,
                        required:true,
                    },
                    riskvalue: {
                        digits:true,
                        required:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackiptype: {
                        required:"请选择IP类型",
                    },
                    blackip:{
                        required:"请输入IP地址",
                        ip:"请输入正确格式的地址.",
                    },
                    riskvalue:{
                        required:"请输入风险值",
                        digits:"请输入数字",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#edit-blackIp-error").html(message).show();
                    } else {
                        $("#edit-blackIp-error").hide();
                    }
                }
            });

            $('#blackIp_search').submit(function(eventdata,event){

                if(!($('#endtime').val()||$('#begintime').val()||$('#blackip').val()||$('#riskvalue').val()||$('#blackiptype0').attr('checked')||$('#blackiptype1').attr('checked'))){
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
/******************************blackurl_high_search***********************/
            $("#blackurl_search").validate({
                rules: {
                    blackurl: {
                        url:true,
                    },
                    riskvalue: {
                        digits:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackurl:{
                        url:"请输入正确格式的地址."
                    },
                    riskvalue:{
                        digits:"请输入正确格式的风险值.",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
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
/******************************blackurl_add*******************************/
            $("#blackurl_add").validate({
                rules: {
                    blackurltype: {//这里每一项对应一项name
                        required:true,
                    },
                    blackurl: {
                        url:true,
                        required:true,
                    },
                    riskvalue: {
                        digits:true,
                        required:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackurltype: {
                        required:"请选择IP类型",
                    },
                    blackurl:{
                        required:"请输入IP地址",
                        url:"请输入正确格式的地址.",
                    },
                    riskvalue:{
                        required:"请输入风险值",
                        digits:"请输入数字",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#add-blackurl-error").html(message).show();
                    } else {
                        $("#add-blackurl-error").hide();
                    }
                }
            });
/******************************blackurl_edit*******************************/
            $("#blackurl_edit").validate({
                rules: {
                    blackurltype: {//这里每一项对应一项name
                        required:true,
                    },
                    blackurl: {
                        url:true,
                        required:true,
                    },
                    riskvalue: {
                        digits:true,
                        required:true,
                        max:100,
                        min:0,
                    },
                },
                messages:{
                    blackurltype: {
                        required:"请选择URL类型",
                    },
                    blackurl:{
                        required:"请输入URL地址",
                        url:"请输入正确格式的地址.",
                    },
                    riskvalue:{
                        required:"请输入风险值",
                        digits:"请输入数字",
                        max:"风险值最大为100",
                        min:"风险值最小为0",
                    },
                },
                invalidHandler: function (form, validator) {
                    var errors = validator.numberOfInvalids();

                    if (errors) {
                        var message = errors == 1 ? 'You had one error. It has been highlighted' : 'You had ' + errors + ' errors. They have been highlighted';
                        $("#edit-blackurl-error").html(message).show();
                    } else {
                        $("#edit-blackurl-error").hide();
                    }
                }
            });

            $('#blackurl_search').submit(function(eventdata,event){
                if(!($('#endtime').val()||$('#begintime').val()||$('#blackurl').val()||$('#riskvalue').val()||$('#blackurltype0').attr('checked')||$('#blackurltype1').attr('checked'))){
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

