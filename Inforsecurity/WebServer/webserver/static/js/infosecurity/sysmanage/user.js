(function( $, window, document, undefined ) {
    $(document).ready(function() {
        var user_list_oTable;
        $('#info').hide();
        
        // Data Tables
        if( $.fn.dataTable ) {
            user_list_oTable = $("#user_list").DataTable({
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
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',//此处的T代表要引用一个插件的意思，为了对后面的单行选中进行支持
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_user_list/",
                "fnServerData":function(sSource,aoData,fnCallback){
                    $.getJSON(sSource,aoData, function (json) { 
                        // Do whatever additional processing you want on the callback, then tell DataTables 
                        $selectrow = null;
                        fnCallback(json);
                    });  
                },
                "aoColumns": [ 
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": true},
                    { "bSearchable": false},
                ],
                "oTableTools":{
                    "sRowSelect": "single",
			        "aButtons": [],
                },
                "aoColumnDefs" : [ 
                    {
                        "aTargets": [8],
                        "fnCreatedCell" : function(nTd, sData, oData, iRow, iCol){
                            var b = $("<button type='button' class='btn' class='btn-group' style='margin-right:5px;'><i class='icon-road'></i>下载证书</button>");
                            b.button();
                            b.on('click',function(){
                                alert(oData[2]);
                                var userid = oData[2];
                                var status = "1"
                                if(status=='0') {
                                    alert("证书正在生成，请等待...");
                                    window.location.reload();
	                            }
                                else{
                                    if(userid!="")
                                    {
                                        var url =  "/static/CA/"+userid+"/setup.zip";                              //only for test
                                        alert(url);
                                        var win = window.open(url,"_parent");                        //open the url
                                        if(win!=null){
                                            win.document.execCommand('SaveAs');                  //download
                                        }
                                        else
                                            alert("打开窗口失败!");
                                    }
                                    else
                                    {
                                        alert("用户ID不存在!");
                                    }
                                }
                                return false;
                            });
                            $(nTd).empty();
                            $(nTd).prepend(b);
                        }
                    },
                ],
            });
        }
    })
}) (jQuery, window, document);
