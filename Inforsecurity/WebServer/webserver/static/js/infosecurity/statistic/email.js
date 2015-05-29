;(function( $, window, document, undefined ) {

    $(document).ready(function() {
        var receiver_detail_oTable;
        var resemails_oTable;
        var resemails_search_oTable;

        var position;
        var contactId="temp0000";
        
        $('#info').hide();

        // Data Tables
        if( $.fn.dataTable ) {
            var alldata = []
    /**********************************resemails and post resemails*****************************************/
            //邮件统计记录和邮件统计记录查找下面的表单
            receiver_detail_oTable = $("#receiver_detail").dataTable({
                "oLanguage":  {
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
                "sAjaxSource": "/ajax/get_resemails_detail_list/",
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
                    if ( aData[0].length >= 20 ){
                        var length = aData[0].length
                        var temphtml = aData[0].toString().substr(0,20)+".....";
                        $('td:eq(0)', nRow).html(temphtml);
                    }
                    $('td:eq(0)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;

                    });
                    $('td:eq(0)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });

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
                            var date = oData[4]
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
                            var id = contactId;
                            var b = $("<button type='button' id='daydetail' class='btn' class='btn-group' style='margin-right:5px;'>当天访问详细</button>");
                            b.button();
                            b.on('click',function(){
                                $("#mws-jui-dialog").dialog("open");
                                $.getJSON('/ajax/dashboard/statistic_email/?emailid='+id+'&datetime='+oData[4], function(data) {
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
                                $.getJSON('/ajax/dashboard/statistic_weekemail/?emailid='+id+'&datetime='+oData[4], function(data) {
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

            //邮件统计记录上面的表单
            resemails_oTable = $("#resemails").dataTable({
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
                "sAjaxSource": "/ajax/get_resemails_list/",
                //"fnServerParams": function(aoData) {
                //    aoData.push({name:"sSearch_4",value:"172.29.142.136",});
                //},
                "aoColumns": [
                    { "bSearchable": false,"bVisible":false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                ],
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    alldata[4] = aData[4]
                    var allphtml4 = aData[5]
                    var allphtml9 = aData[10]
                    var allphtml10 = aData[11]
                    var allphtml11 = aData[12]
                    var allphtml15 = aData[16]
                    if ( aData[5].length >= 5 ){
                        var temphtml = aData[5].toString().substr(0,5)+"....."
                        $('td:eq(4)', nRow).html( temphtml );
                    }
                    if ( aData[10].length >= 5 ){
                        var temphtml = aData[10].toString().substr(0,5)+"....."
                        $('td:eq(9)', nRow).html( temphtml );
                    }
                    if ( aData[11].length >= 5 ){
                        var temphtml = aData[11].toString().substr(0,5)+"....."
                        $('td:eq(10)', nRow).html( temphtml );
                    }
                    if ( aData[12].length >= 5 ){
                        var temphtml = aData[12].toString().substr(0,5)+"....."
                        $('td:eq(11)', nRow).html( temphtml );
                    }
                    if ( aData[16].length >= 5 ){
                        var temphtml = aData[16].toString().substr(0,5)+"....."
                        $('td:eq(15)', nRow).html( temphtml );
                    }
                    $('td:eq(5)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5+5,top:e.pageY+5+5});
                            $("#tip").html(allphtml4);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(5)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(9)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml9);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(9)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(10)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml10);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(10)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(11)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml11);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(11)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(15)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml15);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(15)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        var s = $(node).children();
                        $('#receiver_detail_ip').text("目的ip:" + $(s[6]).text());

                        receiver_detail_oTable.fnReloadAjax();
                    },
                    "aButtons":[],
                },
                "fnDrawCallback": function() {
                    $("#resemails tbody tr").click(function() {
                        position = resemails_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = resemails_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                    });
                }


            });

            //邮件邮件统计记录查找上面的表单
            resemails_search_oTable = $("#resemails_search").dataTable({
                "oLanguage":  {
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
                "sDom": 'T<"top">rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_resemails_list/",
                "fnServerParams": function(aoData) {
                    var i = 0;
                    for(i = 0;i < aoData.length;i++){
                        if(aoData[i]['name'] == 'sSearch_5'){
                            if($('#sip').val()){
                                aoData[i]['value'] = $('#sip').val();
                            }
                        }else if(aoData[i]['name'] == 'sSearch_6'){
                            if($('#dip').val()){
                                aoData[i]['value'] = $('#dip').val();
                            }
                        }else if(aoData[i]['name'] == 'sSearch_3'){
                            if($('#sender').val()){
                                aoData[i]['value'] = $('#sender').val();
                            }
                        }else if(aoData[i]['name'] == 'sSearch_4'){
                            if($('#receiver').val()){
                                aoData[i]['value'] = $('#receiver').val();
                            }
                        }
                    }
                    if($('#riskvalue').val()){
                        aoData.push({name:'riskvalue',value:$('#riskvalue').val()});
                    }
                    if($('#emailtypes').val()){
                        aoData.push({name:'emailtypes',value:$('#emailtypes').val()});
                    }
                    
                    if($('#begintime').val()){
                        aoData.push({name:'begintime',value:$('#begintime').val()});  
                    }

                    if($('#endtime').val()){
                        aoData.push({name:'endtime',value:$('#endtime').val()});  
                    }
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
alldata[4] = aData[4]
                    var allphtml4 = aData[5]
                    var allphtml9 = aData[10]
                    var allphtml10 = aData[11]
                    var allphtml11 = aData[12]
                    if ( aData[5].length >= 10 ){
                        var temphtml = aData[5].toString().substr(0,10)+"....."
                        $('td:eq(4)', nRow).html( temphtml );
                    }
                    if ( aData[10].length >= 10 ){
                        var temphtml = aData[10].toString().substr(0,10)+"....."
                        $('td:eq(9)', nRow).html( temphtml );
                    }
                    if ( aData[11].length >= 10 ){
                        var temphtml = aData[11].toString().substr(0,10)+"....."
                        $('td:eq(10)', nRow).html( temphtml );
                    }
                    if ( aData[12].length >= 10 ){
                        var temphtml = aData[12].toString().substr(0,10)+"....."
                        $('td:eq(11)', nRow).html( temphtml );
                    }
                    $('td:eq(4)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5+5,top:e.pageY+5+5});
                            $("#tip").html(allphtml4);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';
                    });
                    $('td:eq(4)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(9)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml9);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';
                    });
                    $('td:eq(9)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(10)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml10);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';
                    });
                    $('td:eq(10)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                    $('td:eq(11)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml11);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';
                    });
                    $('td:eq(11)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
                "aoColumns": [
                    { "bSearchable": false,"bVisible":false},
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
                    { "bSearchable": false},
                    { "bSearchable": false},
                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        var s = $(node).children();
                        //alert("Selected Row : " + $(s[0]).text());
                        
                        $('#receiver_detail_ip').text("目的ip:" + $(s[6]).text());
                        receiver_detail_oTable.fnReloadAjax();
                    },
                    "aButtons":[],
                },
                "fnDrawCallback": function() {
                    $("#resemails_search tbody tr").click(function() {
                        position = resemails_search_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = resemails_search_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                    });
                }
            });
            
        }
/**********************************resemails and post resemails*****************************************/
        $('#resemails_filter').attr('style','height:25px;');
        $("<button type='button' class='btn' style='float:right;' id='high_search' href='#inline_content'><i class='icon-search'></i>高级搜索</button>").appendTo('#resemails_filter');
        /////定制邮件统计记录查找和邮件记录统计下面的tables
        $("<div class='dataTables_filter' id=receiver_detail_filter></div>").appendTo('#receiver_detail_wrapper div.top');
        $("<div id='receiver_detail_ip'>接受者ip:</div>").appendTo('#receiver_detail_filter');
    });

}) (jQuery, window, document);
