$(function ( $, window, document, undefined ) {
    var chart;
    // alert($("#userid").val());


    $(document).ready(function() {
        $.getJSON("/accounts/get_alarm_count/", function(data) {
                                    // Create the chart
//                                    var x = new Array()
//                                    var y = new Array()
//                                    for(var i=0;i<data.length;i++){
//                                        x[i] = data[i][0];
//                                        y[i] = data[i][1]
//                                    }
            Highcharts.setOptions({                                            // This is for all plots, change Date axis to local timezone
                lang : {
                    months: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],
                    shortMonths: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],
                    weekdays: ['星期一','星期二','星期三','星期四','星期五','星期六','星期日'],
                },
                global : {
                    useUTC : false
                },
            });
            chart = new Highcharts.StockChart({
            
                chart : {	
                    renderTo : 'containerchart',
//                                            type: 'spline'
                },
                rangeSelector: {
                    enabled: false
                },
//                xAxis: {
////.                                           categories: x,
//                    type:"datetime",
//                },  
                title : {
                    text : '报警统计'
                },
                series : [{
                    name : '报警次数',
                    data : data,
                    tooltip: {
                        valueDecimals: 2,
                        xDateFormat:"%Y-%m-%d %H:%M:%S"
                    }
                }]
            });

        });
    })

    // $.getJSON('/ajax/dashboard/get_user_riskvalue', function(data) {
    //         //Create the chart
    //         window.chart = new Highcharts.StockChart({
    //             chart: {
    //                 renderTo: data.pcid+"tb",
    //             },
    //             rangeSelector: {
    //                 buttons: [{
    //                         type: 'all',
    //                         text: '全部'
    //                     }, {
    //                         type: 'minute',
    //                         count: 15,
    //                         text: '15分',
    //                     }, {
    //                         type: 'day',
    //                         count: 1,
    //                         text: '1天'
    //                     }],
    //                 selected: 1,
    //             },
    //             title: {
    //                 text: '用户风险值变化'
    //             },
    //             tooltip:{
    //                 xDateFormat:"%Y-%m-%d %H:%M:%S"
    //             },
    //             yAxis: {
    //                 title: {
    //                     text: '风险值'
    //                 },
    //                 min: 0,
    //                 max: 100,
    //                 minorGridLineWidth: 0, //Width of the minor, secondary grid lines. Defaults to 1.
    //                 gridLineWidth: 0, //The width of the grid lines extending the ticks across the plot area. Defaults to 1
                    
    //                 plotLines: [{
    //                         value: 0,
    //                         color: 'green',
    //                         dashStyle: 'ShortDash',
    //                         width: 2,
    //                         label: {
    //                             text: '风险等级1:0-30'
    //                         }
    //                     }, 
    //                     {
    //                         value: 30,
    //                         color: 'rgba(218, 238, 0, 1)',
    //                         dashStyle: 'ShortDash',
    //                         width: 2,
    //                         label: {
    //                             text: '风险等级2:30-60'
    //                         }
    //                     }, 
    //                     {
    //                         value: 60,
    //                         color: 'rgba(255, 165, 0, 1)',
    //                         dashStyle: 'ShortDash',
    //                         width: 2,
    //                         label: {
    //                             text: '风险等级3:60-85'
    //                         }
    //                     }, {
    //                         value: 85,
    //                         color: 'red',
    //                         dashStyle: 'ShortDash',
    //                         width: 2,
    //                         label: {
    //                             text: '风险等级4:85-100'
    //                         }
    //                     }],
    //             },
    //             subtitle: {
    //                 text: '总体变化情况'
    //             },
    //         // plotOptions: {  
    //         //     line: {  
    //         //         dataGrouping: {  
    //         //             enabled: false  
    //         //         }  
    //         //     }  
    //         // },

    //             series: [{
    //                     name: '风险值',
    //                     data: data.pcchart[0],
    //                 }]
    //         }, function(chart) {
    //             // apply the date pickers
    //             setTimeout(function() {
    //                 $('input.highcharts-range-selector', $('#' + chart.options.chart.renderTo))
    //                 .datepicker()
    //             }, 0)
    //         });
    //     });


});
