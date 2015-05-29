(function( $, window, document, undefined ) {
    $(document).ready(function() {
        var net_behaviour_oTable;
        var net_behaviour_search_oTable;

        var position;
        var contactId="temp0000";
        var detailInfo = "detailTest"
        $('#info').hide();
        
/*********************************blackIp******************************************/
    if( $.fn.dataTable ) {
        var $selectrow = null;

            net_behaviour_oTable = $("#net_behaviour").dataTable({
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
                "sScrollXInner": "150%",
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',//此处的T代表要引用一个插件的意思，为了对后面的单行选中进行支持
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_net_behaviour_list/",
                "fnServerData":function(sSource,aoData,fnCallback){
                    $.getJSON(sSource,aoData, function (json) { 
                        // Do whatever additional processing you want on the callback, then tell DataTables 
                        $selectrow = null;
                        fnCallback(json);
                    });  
                },
                "aoColumns": [
                    { "bSearchable": false, "bVisible": false},
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
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        $selectrow = $(node).children();
                    },
                    "aButtons":[],
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml4 = aData[3];
                    if (aData[3].length >=8){
                        var temphtml = aData[3].toString().substr(0,8)+"....."
                        $('td:eq(2)',nRow).html(temphtml);
                    }
                    $('td:eq(2)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml4);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(2)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
                "fnDrawCallback": function() {
                    $("#blackIp_list tbody tr").click(function() {
                        position = blackiplist_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = blackiplist_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                        detailInfo = blackiplist_oTable.fnGetData(position)[5];
                    });
                }
            });


            
/*********************************blackip_search*****************************************/
            net_behaviour_search_oTable = $("#net_behaviour_search").dataTable({
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
                "sScrollXInner": "101%",
                "sDom": '<"top">rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_net_behaviour_list/",
                "fnServerParams": function(aoData) {
                    var i = 0;

                    for(i = 0;i < aoData.length;i++){
                        // if(aoData[i]['name'] == 'sSearch_2'){
                        //     if($('#level').val()){
                        //         aoData[i]['value'] = $('#level').val();
                        //     }
                        // }
                        // // if(aoData[i]['name'] == 'sSearch_3'){
                        // //     if($('#tick').val()){
                        // //         aoData[i]['value'] = $('#tick').val();
                        // //     }
                        // // }
                        // // if(aoData[i]['name'] == 'sSearch_4'){
                        // //     if($('#version').val()){
                        // //         aoData[i]['value'] = $('#version').val();
                        // //     }
                        // // }
                        // // if(aoData[i]['name'] == 'sSearch_2'){
                        // //     if($('#transfprotc').val()){
                        // //         aoData[i]['value'] = $('#transfprotc').val();
                        // //     }
                        // // }
                        // // if(aoData[i]['name'] == 'sSearch_2'){
                        // //     if($('#appprotc').val()){
                        // //         aoData[i]['value'] = $('#appprotc').val();
                        // //     }
                        // // }
                        // // if(aoData[i]['name'] == 'sSearch_2'){
                        // //     if($('#nettype').val()){
                        // //         aoData[i]['value'] = $('#nettype').val();
                        // //     }
                        // // }
                    }
                    
                    if($('#begintime').val()){
                        aoData.push({name:'begintime',value:$('#begintime').val()});  
                    }

                    if($('#endtime').val()){
                        aoData.push({name:'endtime',value:$('#endtime').val()});  
                    }
                },
                "aoColumns": [
                    { "bSearchable": false,"bVisible": false},
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
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                ],
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml4 = aData[3];
                    if (aData[3].length >=8){
                        var temphtml = aData[3].toString().substr(0,8)+"....."
                        $('td:eq(2)',nRow).html(temphtml);
                    }
                    $('td:eq(2)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml4);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(2)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
            });
            
        }
    /*********************************net_behaviour******************************************/
        // $('#net_behaviour_filter').attr('style','height:25px;');
        // $("<button type='button' class='btn' style='float:right;margin-right:2px;' id='net_behaviour_high_search' href='#inline_content'><i class='icon-search'></i>高级搜索</button> ").appendTo('#net_behaviour_filter');
    
        
    })
}) (jQuery, window, document);
