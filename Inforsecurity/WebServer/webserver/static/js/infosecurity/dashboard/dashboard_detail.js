
$(function() {

    //仪器表
    var clb = document.createElement("clboth");
    clb.style.clear = "both";
    var temparray
    var arraynum = parseInt($("#arraynum").val());
        $.getJSON('/ajax/dashboard/get_angular_data', function(data) {
            for (var i = 0; i < data.pcid.length; i++) 
            {
                temparray = data.pcid;
                var chart = new Highcharts.Chart({
                    chart: {
                        renderTo: data.pcid[i],
                        type: 'gauge',
                        plotBackgroundColor: null,
                        plotBackgroundImage: null,
                        plotBorderWidth: 0,
                        plotShadow: false
                    },
                    title: {
                        text: data.pcid[i]
                    },
                    exporting: {
                        enabled: false //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示 
                    },
                    pane: {
                        startAngle: -150,
                        endAngle: 150,
                        background: [{
                                backgroundColor: {
                                    linearGradient: {x1: 0,y1: 0,x2: 0,y2: 1},
                                    stops: [
                                        [0, '#FFF'], 
                                        [1, '#333']
                                    ]
                                },
                                borderWidth: 0,
                                outerRadius: '109%'
                            }, {
                                backgroundColor: {
                                    linearGradient: {x1: 0,y1: 0,x2: 0,y2: 1},
                                    stops: [
                                        [0, '#333'], 
                                        [1, '#FFF']
                                    ]
                                },
                                borderWidth: 1,
                                outerRadius: '107%'
                            }, {
                            // default background
                            }, {
                                backgroundColor: '#DDD',
                                borderWidth: 0,
                                outerRadius: '105%',
                                innerRadius: '103%'
                            }]
                    },
                    // the value axis
                    yAxis: {
                        min: 0,
                        max: 100,
                        minorTickInterval: 'auto',
                        minorTickWidth: 1,
                        minorTickLength: 10,
                        minorTickPosition: 'inside',
                        minorTickColor: '#666',
                        tickPixelInterval: 30,
                        tickWidth: 2,
                        tickPosition: 'inside',
                        tickLength: 10,
                        tickColor: '#666',
                        labels: {
                            step: 2,
                            rotation: 'auto'
                        },
                        title: {
                            text: '风险值'
                        },
                        plotBands: [{
                                from: 0,
                                to: 30,
                                color: '#55BF3B' // green
                            }, {
                                from: 30,
                                to: 60,
                                color: '#DDDF0D' // yellow
                            }, {
                                from: 60,
                                to: 85,
                                color: '#FF7F00 ' // orange
                            }, {
                                from: 85,
                                to: 100,
                                color: '#DF5353' // red
                            }]
                    },
                    series: [{
                            name: '风险值',
                            data: [data.pcrisk[i]], //数据
                            tooltip: {
                                valueSuffix: ''
                            }
                        }]
                });
            }//end for
        });

    document.getElementById('north').appendChild(clb);


//general_detail用户风险值，访问次数情况

    var arraynum = parseInt($("#arraynum").val());
    
    for (var i = 0; i < arraynum; i++) 
    {
        var pcid = $("#tempindex"+i).val();
        $.getJSON('/ajax/dashboard/get_chart_data?pc='+pcid+'&pcnum='+i, function(data) {
            //Create the chart
            window.chart = new Highcharts.StockChart({
                chart: {
                    renderTo: data.pcid+"tb",
                },
                rangeSelector: {
                    buttons: [{
                            type: 'all',
                            text: '全部'
                        }, {
                            type: 'minute',
                            count: 15,
                            text: '15分',
                        }, {
                            type: 'day',
                            count: 1,
                            text: '1天'
                        }],
                    selected: 1,
                },
                title: {
                    text: '用户风险值变化'
                },
                tooltip:{
                    xDateFormat:"%Y-%m-%d %H:%M:%S"
                },
                yAxis: {
                    title: {
                        text: '风险值'
                    },
                    min: 0,
                    max: 100,
                    minorGridLineWidth: 0, //Width of the minor, secondary grid lines. Defaults to 1.
                    gridLineWidth: 0, //The width of the grid lines extending the ticks across the plot area. Defaults to 1
                    
                    plotLines: [{
                            value: 0,
                            color: 'green',
                            dashStyle: 'ShortDash',
                            width: 2,
                            label: {
                                text: '风险等级1:0-30'
                            }
                        }, 
                        {
                            value: 30,
                            color: 'rgba(218, 238, 0, 1)',
                            dashStyle: 'ShortDash',
                            width: 2,
                            label: {
                                text: '风险等级2:30-60'
                            }
                        }, 
                        {
                            value: 60,
                            color: 'rgba(255, 165, 0, 1)',
                            dashStyle: 'ShortDash',
                            width: 2,
                            label: {
                                text: '风险等级3:60-85'
                            }
                        }, {
                            value: 85,
                            color: 'red',
                            dashStyle: 'ShortDash',
                            width: 2,
                            label: {
                                text: '风险等级4:85-100'
                            }
                        }],
                },
                subtitle: {
                    text: '总体变化情况'
                },
            // plotOptions: {  
            //     line: {  
            //         dataGrouping: {  
            //             enabled: false  
            //         }  
            //     }  
            // },

                series: [{
                        name: '风险值',
                        data: data.pcchart[0],
                    }]
            }, function(chart) {
                // apply the date pickers
                setTimeout(function() {
                    $('input.highcharts-range-selector', $('#' + chart.options.chart.renderTo))
                    .datepicker()
                }, 0)
            });
        });
        
        $.getJSON('/ajax/dashboard/get_chartdt_data?pc='+pcid+'&pcnum='+i, function(data) {
            var containerdtChart = new Highcharts.StockChart({
                chart: {
                    renderTo: data.pcid+"tbdt",
                },
                
                rangeSelector: {
                    buttons: [{
                            type: 'all',
                            text: '全部'
                        }, {
                            type: 'minute',
                            count: 15,
                            text: '15分'
                        }, {
                            type: 'day',
                            count: 1,
                            text: '1天'
                        }],
                    selected: 2
                },
                title: {
                    text: '访问次数情况',
                    align: "left"
                },
                subtitle: {
                    text: '总体变化情况',
                    align: "left"
                },
                legend: {
                    enabled: true,
                    align: "right",
                    floating: true,
                    height: 30,
                    y: -226,
                    x: -80
                },
                yAxis: {
                    minorGridLineWidth: 0, //Width of the minor, secondary grid lines. Defaults to 1.
                    gridLineWidth: 0, //The width of the grid lines extending the ticks across the plot area. Defaults to 1
		        	labels: {
		        		formatter: function() {
		        			return this.value;
		        		}
		        	},
		        	plotLines: [{
		        		value: 0,
		        		width: 2,
		        		color: 'silver'
		        	}]
		        },
            plotOptions: {  
                line: {  
                    dataGrouping: {  
                        enabled: false  
                    }  
                }  
            },
                series: [{//why?
                        name: '邮件访问次数',
                        data: data.pcemailchart,
                        shadow: true,
                    }, 
                    {
                        name: 'ip访问次数',
                        data: data.pcipchart,
                        type: 'spline',
                        shadow: true,
                    }, 
                    {
                        name: 'url访问次数',
                        data: data.pcurlchart,
                        type: 'spline',
                        shadow: true,
                    }]
            }, 
            function(containerdtChart) {
                // apply the date pickers
                setTimeout(function() {
                    $('input.highcharts-range-selector', $(containerdtChart.options.chart.renderTo))
                    .datepicker()
                }, 0)
            });

            // Set the datepicker's date format
            $.datepicker.setDefaults({
                dateFormat: 'yy-mm-dd',
                onSelect: function(dateText) {
                    this.onchange();
                    this.onblur();
                }
            });
            
            Highcharts.setOptions({                                            // This is for all plots, change Date axis to local timezone
                global : {
                    useUTC : false
                },
            });
            
            
        });
        $("#south").append(clb);
        }
    $("#south").append(clb);
});
