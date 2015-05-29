(function( $, window, document, undefined ) {
    $(document).ready(function() {
        var alarm_list_oTable;
        $('#info').hide();
        
        // Data Tables
        if( $.fn.dataTable ) {
            alarm_list_oTable = $("#alarm_list").DataTable({
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
                sPaginationType: "full_numbers",
                "sScrollX": "100%", 
                "sScrollXInner": "100%",                
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',//此处的T代表要引用一个插件的意思，为了对后面的单行选中进行支持
                "bServerSide": true,
                "sAjaxSource": "/usersettings/get_alarm_list/",
                "fnServerData":function(sSource,aoData,fnCallback){
                    $.getJSON(sSource,aoData, function (json) { 
                        // Do whatever additional processing you want on the callback, then tell DataTables 
                        $selectrow = null;
                        fnCallback(json);
                    });  
                },
                "aoColumns": [ 
                    { "bSearchable": false,"bVisible":false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                ],
                "oTableTools":{
                    "sRowSelect": "single",
			        "aButtons": [],
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml = aData[4]
                    if(aData[4].length >= 40){
                        var temphtml3 = aData[4].toString().substr(0,20)+"....."+aData[4].toString().substr(aData[4].length-20,20)
                        $('td:eq(3)', nRow).html( temphtml3 );
                    }
                    $('td:eq(3)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5+5,top:e.pageY+5+5});
                            $("#tip").html(allphtml);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';
                    });
                    $('td:eq(3)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },

            });
        }
    })
}) (jQuery, window, document);
