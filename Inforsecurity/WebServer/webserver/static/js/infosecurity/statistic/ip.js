/********************************************************************************************/
(function( $, window, document, undefined ) {

    $(document).ready(function() {
        var ip_receiver_detail_oTable;
        var resips_search_oTable;
        var resips_oTable;

        var position;
        var contactId="temp0000";
        $('#info').hide();
        // Data Tables
        if( $.fn.dataTable ) {
            ip_receiver_detail_oTable = $("#ip_receiver_detail").dataTable({
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
                
                "sAjaxSource": "/ajax/get_resips_detail_list/",
                "fnServerParams": function(aoData) {
                    var ip;
                    try{
                        ip = contactId;
                    }catch(err){
                        ip = '';
                    }
                    aoData.push({name:'ip',value:ip});
                },
                "aoColumnDefs":[
                    { "bSortable": false, "aTargets": [6]}
                ],
                "aoColumns": [
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                ],
                "aoColumnDefs" : [ 
                    {
                        "aTargets": [8],
                        "fnCreatedCell" : function(nTd, sData, oData, iRow, iCol){
                            var date = oData[5]
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
                            b.button();
                            b.on('click',function(){
                                $("#mws-jui-dialog").dialog("open");
                                $.getJSON('/ajax/dashboard/statistic_ip/?statisticip='+oData[0]+'&datetime='+oData[5], function(data) {
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
                                    Highcharts.setOptions({                                            // This is for all plots, change Date axis to local timezone
                                        global : {
                                            useUTC : false
                                        },
                                    });
                                });

                            });


                            var c = $("<button type='button' id='weekdetail' class='btn' class='btn-group' style='margin-right:5px;'>历史访问详细</button>");
                            c.button();
                            c.on('click',function(){
                                $("#mws-jui-dialog").dialog("open");
                                $.getJSON('/ajax/dashboard/statistic_weekip/?statisticip='+oData[0]+'&datetime='+oData[5], function(data) {
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
                                    Highcharts.setOptions({                                            // This is for all plots, change Date axis to local timezone
                                        global : {
                                            useUTC : false
                                        },
                                    });
                                });
                            });


                            $(nTd).empty();
                            $(nTd).prepend(c);
                            $(nTd).prepend(b);
                        }
                    },
                ]
            });

            resips_oTable = $("#resips").dataTable({
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
                "sAjaxSource": "/ajax/get_resips_list/",

                //"fnServerParams": function(aoData) {
                //    aoData.push({name:"sSearch_4",value:"172.29.142.136",});
                //},
                "aoColumns": [
                    { "bSearchable": false, "bVisible": false},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},

                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        var s = $(node).children();
                        if(resips_oTable.fnGetData(node[0])[11] == "上行"){
                            contactId = $(s[7]).text();
                            $('#ip_receiver_detail_ip').text("远程ip:" + $(s[7]).text());
                        }else{
                            contactId = $(s[6]).text();
                            $('#ip_receiver_detail_ip').text("远程ip:" + $(s[6]).text());
                        }
                        ip_receiver_detail_oTable.fnReloadAjax();
                    },
                    "aButtons":[],
                },
                "fnDrawCallback": function() {
                    $("#resips tbody tr").click(function() {
                        position = resips_oTable.fnGetPosition(this); // getting the clicked row position
                        // contactId = resips_oTable.fnGetData(position)[8]; // getting the value of the first (invisible) column
                    });
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml12 = aData[12];

                    if ( aData[12].length >= 5 ){
                        var temphtml = aData[12].toString().substr(0,5)+"....."
                        $('td:eq(11)', nRow).html( temphtml );
                    }
                    $('td:eq(11)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml12);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(11)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                }
            });


            resips_search_oTable = $("#resips_search").dataTable({
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
                
                "sAjaxSource": "/ajax/get_resips_list/",
                "fnServerParams": function(aoData) {
                    var i = 0;

                    for(i = 0;i < aoData.length;i++){
                        if(aoData[i]['name'] == 'sSearch_7'){
                            if($('#sip').val()){
                                aoData[i]['value'] = $('#sip').val();
                            }
                        }else if(aoData[i]['name'] == 'sSearch_8'){
                            if($('#dip').val()){
                                aoData[i]['value'] = $('#dip').val();
                            }
                        }

                    }

                    if($('#riskvalue').val()){
                        aoData.push({name:'riskvalue',value:$('#riskvalue').val()});
                    }

                    if($('#iptypes').val()){
                        aoData.push({name:'iptypes',value:$('#iptypes').val()});
                    }
                    
                    if($('#begintime').val()){
                        aoData.push({name:'begintime',value:$('#begintime').val()});  
                    }

                    if($('#endtime').val()){
                        aoData.push({name:'endtime',value:$('#endtime').val()});  
                    }
                },
                "aoColumns": [
                    { "bSearchable": false,"bVisible" : false},
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
                    { "bSearchable": false},
                    { "bSearchable": false},
                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        var s = $(node).children();
                        if(resips_search_oTable.fnGetData(node[0])[11] == "上行"){
                            contactId = $(s[7]).text();
                            $('#ip_receiver_detail_ip').text("远程ip:" + $(s[7]).text());
                        }else{
                            contactId = $(s[6]).text();
                            $('#ip_receiver_detail_ip').text("远程ip:" + $(s[6]).text());
                        }
                        ip_receiver_detail_oTable.fnReloadAjax();
                    },
                    "aButtons":[],
                },

            });

        }

        $("<button type='button' class='btn' style='float:right;' id='high_search'><i class='icon-search'></i>高级搜索</button>").appendTo('#resips_filter');
        $("<div class='dataTables_filter' id=ip_receiver_detail_filter></div>").appendTo('#ip_receiver_detail_wrapper div.top');
        $("<div id='ip_receiver_detail_ip'>接受者ip:</div>").appendTo('#ip_receiver_detail_filter');
    });
}) (jQuery, window, document);

