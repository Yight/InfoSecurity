$(function() {
    var $flag = true;
//    $.getJSON('http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function(data) {
    $.getJSON('/ajax/dashboard/general/', function(data) {
        // Create the chart
        window.chart = new Highcharts.StockChart({
            chart: {
                renderTo: 'container',
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
            xAxis:{
                events:{
                    setExtremes: function(e) {
                        if($flag){
                            $.getJSON('/ajax/dashboard/general_update/', 
                                {
                                    min:e.min,
                                    max:e.max,
                                    trigger:e.trigger,
                                },
                                function(newdata) {
                                    $flag = false;
                                    chart.series[0].setData(newdata);
                                    //alert("success");
                                });
                        //   $('#report').html('<b>Set extremes:</b> e.min: '+ Highcharts.dateFormat(null, e.min) + ' | e.max: '+ Highcharts.dateFormat(null, e.max) + ' | e.trigger: ' + e.trigger);
                        }else{
                            $flag = true;
                        }
                    },
                },
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
            series: [{
                    name: '风险值',
                    data: data,
                    marker: {
                        enabled: true,
                        radius: 3
                    },
                    shadow: true,
                    tooltip: {
                        valueDecimals: 2,//what is it mean?
                    }
                }]
        }, function(chart) {
            // apply the date pickers
            setTimeout(function() {
                $('input.highcharts-range-selector', $('#' + chart.options.chart.renderTo))
                .datepicker()
            }, 0)
        });
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
        // lang:{
        //     shortMonths:[__('一月'),__('二月'),__('三月'),__('四月'),
        //                 __('五月'),__('六月'),__('七月'),__('八月'),
        //                 __('九月'),__('十月'),__('十一月'),__('十二月')]
        // }
    });
});


$(function() {

    //general_detail用户风险值，访问次数情况
    var clb = document.createElement("clboth"); //清空格式
    clb.style.clear = "both";
    var cont = 3;
    
    for (var i = 0; i < cont; i++) 
    {
        //生成div，仪器表
        var southDiv = document.createElement("southDiv" + i);
        southDiv.style.width = "500px";
        southDiv.style.height = "300px";
        southDiv.className = "dynamicguagediv";
        
        var southDiv2 = document.createElement("southDiv" + i);
        southDiv2.style.width = "500px";
        southDiv2.style.height = "300px";
        southDiv2.className = "dynamicguagediv";
        
        var container = document.createElement("container" + i);
        container.style.width = "500px";
        container.style.height = "300px";
        
        var containerdt = document.createElement("containerdt" + i);
        containerdt.style.width = "500px";
        containerdt.style.height = "300px";

        //Create the chart
        var containerchart = new Highcharts.StockChart({
            chart: {
                renderTo: container,
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
                text: '用户风险值变化'
            },
            yAxis: {
                title: {
                    text: '风险值'
                },
                min: 0,
                max: 100,
                minorGridLineWidth: 0,
                gridLineWidth: 0,
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
            series: [{
                    name: '风险值',
                    data: "[1131494400000,60.11],[1131580800000,61.18]",
                    marker: {
                        enabled: true,
                        radius: 3
                    },
                    shadow: true,
                    tooltip: {
                        valueDecimals: 2,
                    }
                }]
        }, function(containerChart) {
            // apply the date pickers
            setTimeout(function() {
                $('input.highcharts-range-selector', $(containerChart.options.chart.renderTo)).datepicker();
            }, 0)
        });

        //document.getElementById('south').appendChild(container);
        
        southDiv.appendChild(container);
        $("#south").append(southDiv);
        
        var containerdtChart = new Highcharts.StockChart({
            chart: {
                renderTo: containerdt,
            },
            
            rangeSelector: {
                buttons: [{
                        type: 'all',
                        text: '全部'
                    }, {
                        type: 'minute',
                        count: 3,
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
                title: {
                    text: '访问次数'
                },
                min: 0,
                minorGridLineWidth: 0,
                gridLineWidth: 0,
            },
            series: [{//why?
                    name: '邮件访问次数',
                    data: "[1131494400000,60.11],[1131580800000,61.18]",
                    marker: {
                        enabled: true,
                        radius: 3
                    },
                    shadow: true,
                    tooltip: {
                        valueDecimals: 2
                    }
                }, 
                {
                    name: 'ip访问次数',
                    data: "[1131494400000,60.11],[1131580800000,61.18]",
                    type: 'spline',
                    pointInterval: 15 * 60,//what is it mean?
                    shadow: true,
                    marker: {
                        enabled: true,
                        radius: 4
                    },
                    tooltip: {
                        valueDecimals: 2
                    }
                }, 
                {
                    name: 'url访问次数',
                    data: "[1131494400000,60.11],[1131580800000,61.18]",
                    type: 'spline',
                    pointInterval: 15 * 60,
                    shadow: true,
                    marker: {
                        enabled: true,
                        radius: 4
                    },
                    tooltip: {
                        valueDecimals: 2
                    }
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
        //document.getElementById('south').appendChild(containerdt);
        southDiv2.appendChild(containerdt);
        $("#south").append(southDiv2);
    }
    $("#south").append(clb);
    //document.getElementById('south').appendChild(clb);

    //仪器表
    var gauge = 4;
    var clb = document.createElement("clboth");
    clb.style.clear = "both";
    
    for (var i = 0; i < gauge; i++) 
    {
        var angularContainer = document.createElement("angularContainer" + i);
        angularContainer.style.width = "240px";
        angularContainer.style.height = "240px";
        
        var southDiv = document.createElement("southDiv" + i);
        southDiv.style.width = "240px";
        southDiv.style.height = "240px";
        southDiv.className = "dynamicguagediv";
        
        var chart = new Highcharts.Chart({
            chart: {
                renderTo: angularContainer,
                type: 'gauge',
                plotBackgroundColor: null,
                plotBackgroundImage: null,
                plotBorderWidth: 0,
                plotShadow: false
            },
            title: {
                text: 'Speedometer'
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
                    data: [80], //数据
                    tooltip: {
                        valueSuffix: ''
                    }
                }]
        }, 
        // Add some life
        function(chart) {
            setInterval(function() {
                var point = chart.series[0].points[0], 
                newVal, 
                inc = Math.round((Math.random() - 0.5) * 20);
                
                newVal = point.y + inc;
                if (newVal < 0 || newVal > 200) {
                    newVal = point.y - inc;
                }
                
                point.update(newVal);
            }, 3000);
        });
        document.getElementById('north').appendChild(southDiv);
        southDiv.appendChild(angularContainer);
    }
    document.getElementById('north').appendChild(clb);
});
