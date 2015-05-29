(function( $, window, document, undefined ) {
    $(document).ready(function() {
        var whiteprocesslist_oTable;
        var whiteprocess_list_search_oTable;

        var position;
        var contactId="temp0000";
        var detailInfo = "detailTest"
        $('#info').hide();

        
/*********************************blackIp******************************************/
    if( $.fn.dataTable ) {
        var $selectrow = null;

            whiteprocesslist_oTable = $("#whiteProcess_list").dataTable({
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
                "sDom": 'T<"top"f>rt<"bottom"lpi><"clear">',//此处的T代表要引用一个插件的意思，为了对后面的单行选中进行支持
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_whiteprocess_list/",
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
                    { "bSearchable": false},
                    { "bSearchable": false},
                ],
                "oTableTools":{
                    "sRowSelect": "single",             
                    "fnRowSelected":function(node){
                        $selectrow = $(node).children();
                    },
                    "aButtons":[],
                },
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml4 = aData[5]
                    if (aData[5].length >=10){
                        var temphtml = aData[5].toString().substr(0,10)+"....."
                        $('td:eq(4)',nRow).html(temphtml);
                    }
                    $('td:eq(4)', nRow).hover( function(e) {
                            $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                            $("#tip").html(allphtml4);
                            tip.style.visibility='visible';
                            tip.style.top = event.y+10;
                            tip.style.left = event.x+10;
                            tip.style.maxWidth= ($(window).width()-e.pageX-100)+'px';

                    });
                    $('td:eq(4)', nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
                "fnDrawCallback": function() {
                    $("#whiteProcess_list tbody tr").click(function() {
                        position = whiteprocesslist_oTable.fnGetPosition(this); // getting the clicked row position
                        contactId = whiteprocesslist_oTable.fnGetData(position)[0]; // getting the value of the first (invisible) column
                        detailInfo = whiteprocesslist_oTable.fnGetData(position)[4];
                    });
                }
            });


/*********************************blackip_search*****************************************/
            whiteprocess_list_search_oTable = $("#whiteProcess_list_search").dataTable({
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
                "sDom": '<"top">rt<"bottom"lpi><"clear">',
                "bServerSide": true,
                "sAjaxSource": "/ajax/get_whiteprocess_list/",
                "fnServerParams": function(aoData) {
                    var i = 0;
                    
                    for(i = 0;i < aoData.length;i++){
                        if(aoData[i]['name'] == 'sSearch_3'){
                            if($('#processname').val()){
                                aoData[i]['value'] = $('#processname').val();
                            }
                        }
                        if(aoData[i]['name'] == 'sSearch_4'){
                            if($('#md5').val()){
                                aoData[i]['value'] = $('#md5').val();
                            }
                        }
                        if(aoData[i]['name'] == 'sSearch_6'){
                            if($('#version').val()){
                                aoData[i]['value'] = $('#version').val();
                            }
                        }
                        // if(aoData[i]['name'] == 'sSearch_3'){
                        //     if($('#processname').val()){
                        //         aoData[i]['value'] = $('#processname').val();
                        //     }
                        // }
                    }
//                    if($('#blackip').val()){
//                        aoData.push({name:'blackip',value:$('#blackip').val()});
//                    }

                    // if($('#md5').val()){
                    //     aoData.push({name:'md5',value:$('#md5').val()});
                    // }
                    // if($('#version').val()){
                    //     aoData.push({name:'version',value:$('#version').val()});
                    // }
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
                    { "bSearchable": false},
                    { "bSearchable": false},
                ],
                "fnRowCallback":function(nRow,aData,iDisplayIndex,iDisplayIndexFull){
                    var allphtml4 = aData[5]
                    if (aData[5].length >=15){
                        var temphtml = aData[5].toString().substr(0,15)+"....."
                        $('td:eq(4)',nRow).html(temphtml);
                    }
                    $('td:eq(4)',nRow).hover(function(e){
                        $("#tip").offset({left:e.pageX+5,top:e.pageY+5});
                        $("#tip").html(allphtml4);
                        tip.style.visibility='visible';
                        tip.style.top = event.y+10;
                        tip.style.left = event.x+10;
                        tip.style.maxWidth = ($(window).width()-e.pageX-100)+'px'
                    });
                    $('td:eq(4)',nRow).mouseout(function(e){
                        tip.style.visibility='hidden';
                    });
                },
            });
            
        }
        
    /*********************************blackIp******************************************/
        $('#whiteProcess_list_filter').attr('style','height:25px;');
        $("<button type='button' class='btn' style='float:right;margin-right:2px;' id='whiteProcess_high_search' href='#inline_content'><i class='icon-search'></i>高级搜索</button> <a href='#' class='btn' id='editwhiteProcess'style='float:right;width:66px;margin-right:2px;'><i class='icon-edit'></i>修改</a> <a href='#' class='btn' id='deletewhiteProcess'  style='float:right;width:66px;margin-right:2px;'><i class='icon-remove'></i>删除</a> <a href='#' class='btn' id='addwhiteProcess' style='float:right;width:66px;margin-right:2px;'><i class='icon-plus'></i>添加</a>").appendTo('#whiteProcess_list_filter');
        /*********************************blackIp******************************************/
        //delete one row blackIp
        $("#deletewhiteProcess").bind("click", function (event) {
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
                $.getJSON('/ajax/delete_whiteprocess/', {
                        id:contactId,
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

        //edit one row whiteProcess
        $("#editwhiteProcess").bind("click", function (event) {
            event.preventDefault();
            if($selectrow == null){
                //若当前已经存在add之后的info，则利用opacity 的animate将其slideup
                $('#success').animate({ opacity:0 }, function() {
			        $(this).slideUp("fast", function() {
				         $(this).css("opacity", '');
			        });
		        });

                //删除info dom旧的内容和样式
                $('#info').removeClass('error').removeClass('success').text('请选择一条记录再修改!');

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
                event.preventDefault();
                $('#edit_processname').val($($selectrow[2]).text());
                $('#editmd5').val($($selectrow[3]).text());
                $('#editdescription').val(detailInfo);
                $('#editversion').val($($selectrow[5]).text());
                
                $("#whiteProcess_edit_dialog").dialog("open");

                $('#whiteProcess_edit').submit(function(eventdata,event){


					$.getJSON('/ajax/edit_whiteprocess/', {
							id:contactId,
                            processname:$('#edit_processname').val(),
                            md5:$('#editmd5').val(),
                            description:$('#editdescription').val(),
                            version:$('#editversion').val(),
						},
						function(data){
							if(data == 'true'){

								//修改datatables
                                $($selectrow[2]).text($('#edit_processname').val());
                                $($selectrow[3]).text($('#editmd5').val());
                                $($selectrow[4]).text($('#editdescription').val());
                                $($selectrow[5]).text($('#editversion').val());

                                
                                //关闭dialog
                                $("#whiteProcess_edit_dialog").dialog("close");
                                
								//若当前已经存在add之后的info，则利用opacity 的animate将其slideup
								$('#success').animate({ opacity:0 }, function() {
									$(this).slideUp("fast", function() {
										$(this).css("opacity", '');
									});
								});

								//删除info dom旧的内容和样式
								$('#info').removeClass('error').removeClass('warning').text('修改成功!');

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
								whiteprocesslist_oTable.fnReloadAjax();
							}else if(data == 'false'){
                                $("#whiteProcess_edit_dialog").dialog("close");

								//若当前已经存在add之后的info，则利用opacity 的animate将其slideup
								$('#success').animate({ opacity:0 }, function() {
									$(this).slideUp("normal", function() {
										$(this).css("opacity", '');
									});
								});

								//删除info dom旧的内容和样式
								$('#info').removeClass('success').removeClass('warning').text('修改失败!');

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
                    //此处有问题，但是能达到效果,可以在以后修改
                    event.preventDefault();
                });
            }
        });
    })
}) (jQuery, window, document);
