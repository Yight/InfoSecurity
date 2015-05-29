;(function( $, window, document, undefined ) {
    $(document).ready(function() {
        var register_list_oTable;

        $('#info').hide();
        // Data Tables
        if( $.fn.dataTable ) {
            register_list_oTable = $("#register_list").dataTable({
                "oLanguage": {
                    "sProcessing":   "处理中...",
                    "sLengthMenu":   "显示 _MENU_ 项结果",
                    "sZeroRecords":  "没有匹配结果",
                    "sInfo":         "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                    "sInfoEmpty":    "显示第 0 至 0 项结果，共 0 项",
                    "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                    "sInfoPostFix":  "",
                    "sSearch":       "快速搜索:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "首页",
                        "sPrevious": "上页",
                        "sNext":     "下页",
                        "sLast":     "末页"
                    }
                },
                "iDisplayLength": 10,
                "bAutoWidth": false,
                "bDeferRender": true,//Deferred rendering
                "bProcessing": true,
                "aLengthMenu": [[10, 20, 30], [10, 20, 30]],
                "sPaginationType": "full_numbers",
                "sScrollX": "100%",
                "sScrollXInner": "100%",
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',//此处的T代表要引用一个插件的意思，为了对后面的单行选中进行支持
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_register_list/",
                "fnServerData":function(sSource,aoData,fnCallback){
                    $.getJSON(sSource,aoData, function (json) { 
                        // Do whatever additional processing you want on the callback, then tell DataTables 
                        $selectrow = null;
                        fnCallback(json);
                    });  
                },
                "oTableTools":{
                    "sRowSelect": "multi",
                    "fnRowSelected":function(node){
                        $selectrow = $(node).children();
                        jQuery(node).find("input[type=checkbox]").attr("checked", true);
                    },
                    "fnRowDeselected": function ( node ) {
                        jQuery(node).find("input[type=checkbox]").attr("checked", false);
                    },
                    
			        "aButtons": [ "select_all", "select_none" ],
                },
                "aoColumns": [
                    { "bSearchable": true,"bSortable": false},
                    { "bSearchable": true,"bVisible": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": true},
                ],
            });
        }
        
        $('.DTTT_container').hide();
        
        var checked  = 0;
        $('#testcheckbox').click(function(){
            if (checked == 1)
            {
                checked  = 0
                jQuery("#register_list").find("input[type=checkbox]").attr("checked", false);
                jQuery("#register_list").find('tr').removeClass("DTTT_selected");
            }
            else
            {
                checked = 1;
                jQuery("#register_list").find('tr').addClass("DTTT_selected");
                jQuery("#register_list").find("input[type=checkbox]").attr("checked", true);
            }
            
        });
        
        $('#register_list').attr('style','height:25px;');
        $("<button type='button' class='btn' style='float:right;margin-right:2px;' id='pass' href='#inline_content'><i class='icon-search'></i>通过</button> <a href='#' class='btn' id='reject'style='float:right;width:66px;margin-right:2px;'><i class='icon-edit'></i>拒绝</a>").appendTo('#register_list_filter');
        
        $("#pass").bind("click", function (event) {
            var allvalue = fnGetIdsOfSelectedRows(fnGetSelected(register_list_oTable)).toString();
            $.getJSON('/ajax/prove_user/', {
                id:allvalue,
                type:true,
            });
            register_list_oTable.fnReloadAjax();
            var message = "通过请求"
            $("#passorreject").html(message).show();
        });

        $("#reject").bind("click", function (event) {
            var allvalue = fnGetIdsOfSelectedRows(fnGetSelected(register_list_oTable)).toString();
            $.getJSON('/ajax/prove_user/', {
                id:allvalue,
                type:false,
            });
            register_list_oTable.fnReloadAjax();
            var message = "没有通过请求"
            $("#passorreject").html(message).show();
        });
        //获得选择的行
        function fnGetSelected(oTableLocal) {
            var aReturn = new Array();
            var aTrs = oTableLocal.fnGetNodes();
            for (var i = 0; i < aTrs.length; i++) {
                if ($(aTrs[i]).hasClass('DTTT_selected')) {
                    aReturn.push(aTrs[i]);
                }
            }
            return aReturn;
        }
        //获得所选择行的某一列的值
        function fnGetIdsOfSelectedRows(oSelectedRows) {
            var aRowIndexes = new Array();
            var aRowData = new Array();
            var aReturn = new Array();
            var AllValues;
            
            aRowIndexes = oSelectedRows;    
            for(var i = 0; i < aRowIndexes.length; i++){
                aRowData = register_list_oTable.fnGetData(aRowIndexes[i]);
                AllValues = aRowData[1];
                aReturn.push(AllValues);
            }
            return aReturn;
        }
        
    })
}) (jQuery, window, document);
