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
        if( $.fn.dialog  ) {
        
            $("#mws-form-dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#mws-validate').submit();
                    },
                },
            });
/******************************url-search-validate***********************/
            $("#url-search-form-dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#url-search-validate').submit();
                    },
                },
            });
            
/******************************ip-search-validate***********************/
            $("#ip-search-form-dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#ip-search-validate').submit();
                    },
                },
            });
            
/******************************blackemail_high_search***********************/
            $("#blackemail_search_dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function(event,ui) {
                        $('#blackemail_search').submit();
                    },
                },
            });
/******************************white_ip_add********************************/
            $("#white_ip_add_dialog").dialog({
                autoOpen: false,
                title: "添加IP白名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#white_ip_add').submit();
                    },
                },
            });
            $("#addwhiteip").bind("click", function (event) {
                $("#white_ip_add_dialog").dialog("open");
                event.preventDefault();
            });
/******************************white_url_add********************************/
            $("#white_url_add_dialog").dialog({
                autoOpen: false,
                title: "添加URL白名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#white_url_add').submit();
                    },
                },
            });
            $("#addwhiteurl").bind("click", function (event) {
                $("#white_url_add_dialog").dialog("open");
                event.preventDefault();
            });
/******************************white_email_add********************************/
            $("#white_email_add_dialog").dialog({
                autoOpen: false,
                title: "添加Email白名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#white_email_add').submit();
                    },
                },
            });
            $("#addwhiteemail").bind("click", function (event) {
                $("#white_email_add_dialog").dialog("open");
                event.preventDefault();
            });


/******************************whiteProcess_high_search***********************/
            $("#whiteProcess_search_dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function(event,ui) {
                        $('#whiteProcess_search').submit();
                    },
                },
            });
/******************************whiteProcess_add********************************/
            $("#whiteProcess_add_dialog").dialog({
                autoOpen: false,
                title: "添加黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#whiteProcess_add').submit();
                    },
                },
            });
/******************************whiteProcess_edit********************************/
            $("#whiteProcess_edit_dialog").dialog({
                autoOpen: false,
                title: "修改黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"edit",
                    text:"确定",
                    click: function (event,ui) {
                        $('#whiteProcess_edit').submit();
                    },
                }]
            });





/******************************blackemail_add********************************/
            $("#blackemail_add_dialog").dialog({
                autoOpen: false,
                title: "添加黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#blackemail_add').submit();
                    },
                },
            });
    /******************************blackemail_edit********************************/
            $("#blackemail_edit_dialog").dialog({
                autoOpen: false,
                title: "修改黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"edit",
                    text:"确定",
                    click: function (event,ui) {
                        $('#blackemail_edit').submit();
                    },
                }]
            });
            
            
/******************************blackIp_high_search***********************/
            $("#blackIp_search_dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function(event,ui) {
                        $('#blackIp_search').submit();
                    },
                },
            });
    /******************************blackIp_add********************************/
            $("#blackIp_add_dialog").dialog({
                autoOpen: false,
                title: "添加黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#blackIp_add').submit();
                    },
                },
            });
    /******************************blackIp_edit********************************/
            $("#blackIp_edit_dialog").dialog({
                autoOpen: false,
                title: "修改黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"edit",
                    text:"确定",
                    click: function (event,ui) {
                        $('#blackIp_edit').submit();
                    },
                }]
            });
    /******************************blackurl_add********************************/
            $("#blackurl_add_dialog").dialog({
                autoOpen: false,
                title: "添加黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function (event,ui) {
                        $('#blackurl_add').submit();
                    },
                },
            });
    /******************************blackurl_edit********************************/
            $("#blackurl_edit_dialog").dialog({
                autoOpen: false,
                title: "修改黑名单",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: [{
                    id:"edit",
                    text:"确定",
                    click: function (event,ui) {
                        $('#blackurl_edit').submit();
                    },
                }]
            });
            
/******************************blackurl_high_search***********************/
            $("#blackurl_search_dialog").dialog({
                autoOpen: false,
                title: "高级查找",
                modal: true,
                width: "400",
                closeText:"hide",
                buttons: {
                    "确定": function(event,ui) {
                        $('#blackurl_search').submit();
                    },
                },
            });
/******************************blackurl_high_search***********************/
            $("#mws-jui-dialog").dialog({
                autoOpen: false,
                title: "访问详细",
                modal: true,
                width: "640",
                height: "540",
                closeText:"hide",
                buttons: {
                    "关闭": function(event,ui) {
                        $("#mws-jui-dialog").dialog("close");
                    },
                },
            });            
        } 

        $("#daydetail").bind("click", function (event) {
            $("#mws-jui-dialog").dialog("open");
            $("#url-search-form-dialog").dialog("open");
            $("#ip-search-form-dialog").dialog("open");
            event.preventDefault();
        });


        $("#high_search").bind("click", function (event) {
            $("#mws-form-dialog").dialog("open");
            $("#url-search-form-dialog").dialog("open");
            $("#ip-search-form-dialog").dialog("open");
            event.preventDefault();
        });

        if( $.fn.button  ) {
            $("#email_type").buttonset();
            $("#ip_type").buttonset();
            $("#url_type").buttonset();
        }

        if( $.fn.datepicker ) {
            $(".mws-datepicker").datepicker({
                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
                constrainInput: true,
                maxDate:"+0d",
            });
        }
        

/******************************whiteProcess_high_search***********************/
        $("#whiteProcess_high_search").bind("click", function (event) {
            $("#whiteProcess_search_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#whiteProcess_type").buttonset();
        }

        if( $.fn.datepicker ) {
            $("#whiteProcess_search .mws-datepicker").datepicker({
                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
                constrainInput: true,
                maxDate:"+0d",
            });
        }
    /******************************whiteProcess_add********************************/
        $("#addwhiteProcess").bind("click", function (event) {
            $("#whiteProcess_add_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#whiteProcess_type_add").buttonset();
        }
    /******************************whiteProcess_edit********************************/
        
        if( $.fn.button  ) {
            $("#whiteProcess_type_edit").buttonset();
        }
        

    
/******************************blackemail_high_search***********************/
        $("#blackemail_high_search").bind("click", function (event) {
            $("#blackemail_search_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#blackemail_type").buttonset();
        }

        if( $.fn.datepicker ) {
            $("#blackemail_search .mws-datepicker").datepicker({
                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
                constrainInput: true,
                maxDate:"+0d",
            });
        }
    /******************************blackemail_add********************************/
        $("#addblackemail").bind("click", function (event) {
            $("#blackemail_add_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#blackemail_type_add").buttonset();
        }

    /******************************blackemail_edit********************************/
        
        if( $.fn.button  ) {
            $("#blackemail_type_edit").buttonset();
        }
/******************************blackip_high_search***********************/
        $("#blackIp_high_search").bind("click", function (event) {
            $("#blackIp_search_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#blackIp_type").buttonset();
        }

        if( $.fn.datepicker ) {
            $("#blackIp_search .mws-datepicker").datepicker({
                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
                constrainInput: true,
                maxDate:"+0d",
            });
        }
/******************************blackIp_add********************************/
        $("#addblackIp").bind("click", function (event) {
            $("#blackIp_add_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#blackIp_type_add").buttonset();
        }
/******************************blackIp_edit********************************/
        
        if( $.fn.button  ) {
            $("#blackIp_type_edit").buttonset();
        }
        
/******************************blackurl_high_search***********************/
        $("#blackurl_high_search").bind("click", function (event) {
            $("#blackurl_search_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#blackurl_type").buttonset();
        }

        if( $.fn.datepicker ) {
            $("#blackurl_search .mws-datepicker").datepicker({
                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
                constrainInput: true,
                maxDate:"+0d",
            });
        }

/******************************blackurl_add********************************/
        $("#addblackurl").bind("click", function (event) {
            $("#blackurl_add_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#blackurl_type_add").buttonset();
        }
/******************************blackurl_edit********************************/
        
        if( $.fn.button  ) {
            $("#blackurl_type_edit").buttonset();
        }


/*===================================net_behaviour_high_search==========================*/
        $("#net_behaviour_search_dialog").dialog({
            autoOpen: false,
            title: "高级查找",
            modal: true,
            width: "400",
            closeText:"hide",
            buttons: {
                "确定": function(event,ui) {
                    $('#net_behaviour_search').submit();
                },
            },
        });

        $("#net_behaviour_high_search").bind("click", function (event) {
            $("#net_behaviour_search_dialog").dialog("open");
            event.preventDefault();
        });
        
        if( $.fn.button  ) {
            $("#net_behaviour_type").buttonset();
        }

        if( $.fn.datepicker ) {
            $("#net_behaviour_search .mws-datepicker").datepicker({
                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
                constrainInput: true,
                maxDate:"+0d",
            });
        }

    });
}) (jQuery, window, document);
