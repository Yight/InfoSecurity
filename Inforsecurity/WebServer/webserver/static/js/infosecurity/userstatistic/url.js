/********************************************************************************************/
(function( $, window, document, undefined ) {

    $(document).ready(function() {
        var url_receiver_detail_oTable;
        var receiver_search_oTable;
        var receiver_oTable;
        
        var position;
        var contactId="temp0000";
        $('#info').hide();
        // Data Tables
        if( $.fn.dataTable ) {
            var alldata = []
            url_receiver_detail_oTable = $("#url_receiver_detail").dataTable({
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
                "iDisplayLength": 3,
                "bAutoWidth": false,
                "bDeferRender": true,//Deferred rendering
                "bProcessing": true,
                "aLengthMenu": [[3, 4, 5], [3, 4, 5]],
                sPaginationType: "full_numbers",
                "sScrollX": "100%",
                "sScrollXInner": "120%",
                "sDom": '<"top">rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                
                "sAjaxSource": "/ajax/get_user_resurls_detail_list/",
                "fnServerParams": function(aoData) {
                    var id;
                    try{
                        id = contactId;
                    }catch(err){
                        id = '';
                    }
                    aoData.push({name:'id',value:id});
                },
                "aoColumnDefs":[
                    { "bSortable": false, "aTargets": [6]}
                ],
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml = aData[0];
                    if ( aData[0].length >= 50 ){
                        var length = aData[0].length
                        var temphtml = aData[0].toString().substr(0,25)+"....."+aData[0].toString().substr(aData[0].length-25,25);
                        $('td:eq(0)', nRow).html(temphtml);
                    }
                    $('td:eq(0)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-50)+'px';

                    });
                    $('td:eq(0)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
//                    $('td:eq(6)',nRow).html("<div class='btn-group'><button type='button' class='btn' style='margin-right:5px;'><i class='icon-road'></i>当天访问详细</button><button type='button' class='btn' style='margin-left:5px;'><i class='icon-road'></i>历史访问详细</button></div>"); 
                },
                "fnCreatedRow":function(nRow,aData,iDataIndex){
                   // $('td:eq(7)',nRow).addClass('little_padding');
                    $('td:eq(6)',nRow).attr('style','padding:1px;');
                },
                "aoColumns": [
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                ],
                "aoColumnDefs" : [ 
                    {
                        "aTargets": [6],
                        "fnCreatedCell" : function(nTd, sData, oData, iRow, iCol){
                            var date = oData[3]
                            historydate = new Date(date)
                            var year = historydate.getFullYear()
                            var month = historydate.getMonth()+1
                            var day = historydate.getDate()
                            day = day-6
                            var weekago = new Date(year,month,day)
                            year = weekago.getFullYear()
                            month = weekago.getMonth()
                            day = weekago.getDate()
                            weekago = year+'-'+month+'-'+day
                            var b = $("<button type='button' id='daydetail' class='btn' class='btn-group' style='margin-right:5px;'>当天访问详细</button>");
                            var id = contactId;
                            b.button();
                            b.on('click',function(){
                                $("#mws-jui-dialog").dialog("open");
                                $.getJSON('/ajax/dashboard/userstatistic_url/?urlid='+id+'&datetime='+oData[3], function(data) {
                                    // Create the chart
                                    window.chart = new Highcharts.StockChart({
                                        chart : {
                                            renderTo : 'container'
                                        },
                                        rangeSelector: {
                                            enabled: false
                                        },
                                        title : {
                                            text : '当天访问详细('+date+')'
                                        },
                                        
                                        series : [{
                                            name : '访问次数',
                                            data : data,
                                            tooltip: {
                                                valueDecimals: 2
                                            }
                                        }]
                                    });
                                });

                            });


                            var c = $("<button type='button' id='weekdetail' class='btn' class='btn-group' style='margin-right:5px;'>历史访问详细</button>");
                            c.button();
                            c.on('click',function(){
                                $("#mws-jui-dialog").dialog("open");
                                $.getJSON('/ajax/dashboard/userstatistic_weekurl/?urlid='+id+'&datetime='+oData[3], function(data) {
                                    // Create the chart
                                    window.chart = new Highcharts.StockChart({
                                        chart : {
                                            renderTo : 'container'
                                        },
                                        rangeSelector: {
                                            enabled: false
                                        },
                                        title : {
                                            text : '历史访问详细('+weekago+'至'+date+')'
                                        },
                                        
                                        series : [{
                                            name : '访问次数',
                                            data : data,
                                            tooltip: {
                                                valueDecimals: 2
                                            }
                                        }]
                                    });
                                });
                            });
                            Highcharts.setOptions({                                            // This is for all plots, change Date axis to local timezone
                                global : {
                                    useUTC : false
                                },
                            });

                            $(nTd).empty();
                            $(nTd).prepend(c);
                            $(nTd).prepend(b);
                        }
                    },
                ]
            });

            receiver_oTable = $("#resurls").dataTable({
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
                "aLengthMenu": [[10, 20, 30], [10, 20, 30]],
                sPaginationType: "full_numbers",
                "bAutoWidth": false,
                "sScrollX": "100%",
                "bDeferRender": true,//Deferred rendering
                "bProcessing": true,
                //"bStateSave": true,
                "sScrollXInner": "150%",
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_user_resurls_list/",

                //"fnServerParams": function(aoData) {
                //    aoData.push({name:"sSearch_4",value:"172.29.142.136",});
                //},
                "aoColumns": [
                    { "bSearchable": false,"bVisible": false},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": false},
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
                        var s = $(node).children();
                        //alert("Selected Row : " + $(s[0]).text());
                        
                        $('#url_receiver_detail_ip').text("目的ip:" + $(s[6]).text());
                        url_receiver_detail_oTable.fnReloadAjax();
                    },
                    "aButtons":[],
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml = aData[3];
                    alldata[3] = aData[3];
                    if ( aData[3].length >= 30 ){
                        var length = aData[3].length
                        var temphtml = aData[3].toString().substr(0,15)+"....."+aData[3].toString().substr(aData[3].length-15,15);
                        $('td:eq(2)', nRow).html( temphtml );
                    }
                    $('td:eq(2)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-50)+'px';

                    });
                    $('td:eq(2)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
                "aoColumnDefs" : [ 
                    {
                        "aTargets": [12],
                        "fnCreatedCell" : function(nTd, sData, oData, iRow, iCol){
                            var b = $("<button type='button' class='btn' class='btn-group' style='margin-right:5px;'><i class='icon-road'></i>加入白名单</button>");
                            b.button();
                            b.on('click',function(){
                                $.getJSON('/ajax/add_white_url/', {
                                    white_url:oData[3],
                                    id:oData[0],
                                    
                                });
//                                var oTable = $('#resemails').dataTable();
                                receiver_oTable.fnReloadAjax();
                                return false;
                            });
                            $(nTd).empty();
                            $(nTd).prepend(b);
                        }
                    },
                ],
                "fnDrawCallback": function() {
                    $("#resurls tbody tr").click(function() {
                        position = receiver_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = receiver_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                    });
                }

            });


            receiver_search_oTable = $("#resurls_search").dataTable({
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
                "sScrollXInner": "150%",
                "sDom": 'T<"top">rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                
                "sAjaxSource": "/ajax/get_user_resurls_list/",
                "fnServerParams": function(aoData) {
                    var i = 0;

                    for(i = 0;i < aoData.length;i++){
                        if(aoData[i]['name'] == 'sSearch_6'){
                            if($('#sip').val()){
                                aoData[i]['value'] = $('#sip').val();
                            }
                        }else if(aoData[i]['name'] == 'sSearch_7'){
                            if($('#dip').val()){
                                aoData[i]['value'] = $('#dip').val();
                            }
                        }else if(aoData[i]['name'] == 'sSearch_3'){
                            if($('#url').val()){
                                aoData[i]['value'] = $('#url').val();
                            }
                        }
                    }

                    if($('#urltypes').val()){
                        aoData.push({name:'urltypes',value:$('#urltypes').val()});
                    }

                    if($('#riskvalue').val()){
                        aoData.push({name:'riskvalue',value:$('#riskvalue').val()});
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
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        var s = $(node).children();
                        //alert("Selected Row : " + $(s[0]).text());
                        
                        $('#url_receiver_detail_ip').text("接受者ip:" + $(s[6]).text());
                        url_receiver_detail_oTable.fnReloadAjax();
                    },
                    "aButtons":[],
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml = aData[3];
                    if ( aData[3].length >= 50 ){
                        var length = aData[3].lengthl
                        var temphtml = aData[3].toString().substr(0,25)+"....."+aData[3].toString().substr(aData[3].length-25,25);
                        $('td:eq(2)', nRow).html( temphtml );
                    }
                    $('td:eq(2)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-50)+'px';

                    });
                    $('td:eq(2)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
                "aoColumnDefs" : [ 
                    {
                        "aTargets": [12],
                        "fnCreatedCell" : function(nTd, sData, oData, iRow, iCol){
                            var b = $("<button type='button' class='btn' class='btn-group' style='margin-right:5px;'><i class='icon-road'></i>加入白名单</button>");
                            b.button();
                            b.on('click',function(){
                                $.getJSON('/ajax/add_white_url/', {
                                    white_url:oData[3],
                                    id:oData[0],
                                    
                                });
//                                var oTable = $('#resemails').dataTable();
                                receiver_search_oTable.fnReloadAjax();
                                return false;
                            });
                            $(nTd).empty();
                            $(nTd).prepend(b);
                        }
                    },
                ],
                "fnDrawCallback": function() {
                    $("#resurls_search tbody tr").click(function() {
                        position = receiver_search_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = receiver_search_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                    });
                }
            });

        }
        $("<button type='button' class='btn' style='float:right;' id='high_search' href='#inline_content'><i class='icon-search'></i>高级搜索</button>").appendTo('#resurls_filter');
        $("<div class='dataTables_filter' id=url_receiver_detail_filter></div>").appendTo('#url_receiver_detail_wrapper div.top');
        $("<div id='url_receiver_detail_ip'>接受者ip:</div>").appendTo('#url_receiver_detail_filter');
    });
}) (jQuery, window, document);

