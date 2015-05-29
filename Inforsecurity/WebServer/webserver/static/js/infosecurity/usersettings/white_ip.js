(function( $, window, document, undefined ) {
$(document).ready(function() {
        var whiteiplist_oTable;
        $('#info').hide();
        var position;
        var contactId="temp0000";
/*********************************whiteiplist******************************************/
    if( $.fn.dataTable ) {
        var $selectrow = null;

            whiteiplist_oTable = $("#white_ip_list").dataTable({
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
                "sScrollXInner": "101%",
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',//此处的T代表要引用一个插件的意思，为了对后面的单行选中进行支持
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_white_ip_list/",
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
                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        $selectrow = $(node).children();
                    },
                    "aButtons":[],
                },
                "fnDrawCallback": function() {
                    $("#white_ip_list tbody tr").click(function() {
                        position = whiteiplist_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = whiteiplist_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                    });
                }
            });
        }
/*********************************white_ip_list******************************************/
        $('#white_ip_list_filter').attr('style','height:25px;');
        $("<a href='#' class='btn' id='deleteblackIp'  style='float:right;width:66px;margin-right:2px;'><i class='icon-remove'></i>删除</a> <a href='#' class='btn' id='addwhiteip' style='float:right;width:66px;margin-right:2px;'><i class='icon-plus'></i>添加</a>").appendTo('#white_ip_list_filter');
/*********************************blackIp******************************************/

        //delete one row blackIp
        $("#deleteblackIp").bind("click", function (event) {
            event.preventDefault();
            if($selectrow == null){
                //若当前已经存在add之后的info，则利用opacity 的animate将其slideup
                $('#success').animate({ opacity:0 }, function() {
			        $(this).slideUp("fast", function() {
				         $(this).css("opacity", '');
			        });
		        });

                //删除info dom旧的内容和样式
                $('#info').removeClass('error').removeClass('success').text('请选择一条记录再删除!');

                //添加warning
                $('#info').addClass('mws-form-message warning').animate({ opacity:1 }, function() {
		            $(this).slideDown("fast", function() {
			            $(this).css("", 'opacity');
		            });
	            });

                //重新刷新js，为了使新添加的js能支持click后opacity特性
		        // Form Messages 
                $(".mws-form-message").on("click", function() {
		            $(this).animate({ opacity:0 }, function() {
			            $(this).slideUp("fast", function() {
				            $(this).css("opacity", '');
			            });
		            });
	            });
            }else{
                $.getJSON('/ajax/delete_white_ip/', {
                        id:contactId,
                        ip:$($('table[name="white_ip_list"] tbody tr.DTTT_selected td')[1]).text(),
                    },
                    function(data){
                        if(data == 'true'){
                            //若当前已经存在add之后的info，则利用opacity 的animate将其slideup
                            $('#success').animate({ opacity:0 }, function() {
			                    $(this).slideUp("fast", function() {
    				                $(this).css("opacity", '');
	    		                });
		                    });

                            //删除info dom旧的内容和样式
                            $('#info').removeClass('error').removeClass('warning').text('删除成功!');

                            //添加success
                            $('#info').addClass('mws-form-message success').animate({ opacity:1 }, function() {
		                        $(this).slideDown("fast", function() {
			                        $(this).css("", 'opacity');
		                        });
	                        });
                            //$('#info').addClass('mws-form-message success').animate({ opacity:1 });

                            //重新刷新js，为了使新添加的js能支持click后opacity特性
		                    // Form Messages 
                            $(".mws-form-message").on("click", function() {
		                        $(this).animate({ opacity:0 }, function() {
			                        $(this).slideUp("fast", function() {
				                        $(this).css("opacity", '');
			                        });
		                        });
	                        });
                            $($selectrow).remove();
                            $selectrow = null;
                            whiteiplist_oTable.fnReloadAjax();
                        }else if(data == 'false'){
                            //若当前已经存在add之后的info，则利用opacity 的animate将其slideup
                            $('#success').animate({ opacity:0 }, function() {
			                    $(this).slideUp("normal", function() {
    				                $(this).css("opacity", '');
	    		                });
		                    });

                            //删除info dom旧的内容和样式
                            $('#info').removeClass('success').removeClass('warning').text('删除失败!');

                            //添加fail
                            $('#info').addClass('mws-form-message error').animate({ opacity:1 }, function() {
		                        $(this).slideDown("fast", function() {
			                        $(this).css("", 'opacity');
		                        });
	                        });

                            //重新刷新js，为了使新添加的js能支持click后opacity特性
		                    // Form Messages 
                            $(".mws-form-message").on("click", function() {
		                        $(this).animate({ opacity:0 }, function() {
			                        $(this).slideUp("fast", function() {
				                        $(this).css("opacity", '');
			                        });
		                        });
	                        });
                        }
                 });
            }
        });
    })
}) (jQuery, window, document)
