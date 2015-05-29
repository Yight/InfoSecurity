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
            // yAxis: {
            //     title: {
            //         text: '风险值'
            //     },
            //     min: 0,
            //     max: 100,
            //     minorGridLineWidth: 0, //Width of the minor, secondary grid lines. Defaults to 1.
            //     gridLineWidth: 0, //The width of the grid lines extending the ticks across the plot area. Defaults to 1
            //     plotLines: [{
            //             value: 0,
            //             color: 'green',
            //             dashStyle: 'ShortDash',
            //             width: 2,
            //             label: {
            //                 text: '风险等级1:0-30'
            //             }
            //         }, 
            //         {
            //             value: 30,
            //             color: 'rgba(218, 238, 0, 1)',
            //             dashStyle: 'ShortDash',
            //             width: 2,
            //             label: {
            //                 text: '风险等级2:30-60'
            //             }
            //         }, 
            //         {
            //             value: 60,
            //             color: 'rgba(255, 165, 0, 1)',
            //             dashStyle: 'ShortDash',
            //             width: 2,
            //             label: {
            //                 text: '风险等级3:60-85'
            //             }
            //         }, {
            //             value: 85,
            //             color: 'red',
            //             dashStyle: 'ShortDash',
            //             width: 2,
            //             label: {
            //                 text: '风险等级4:85-100'
            //             }
            //         }],
            // },
            subtitle: {
                text: '总体变化情况'
            },
            plotOptions: {  
                line: {  
                    dataGrouping: {  
                        enabled: false  
                    }  
                }  
            }, 
            series: [{
                    name: '风险值',
                    data: data,
                    // marker: {
                    //     enabled: true,
                    //     radius: 3
                    // },
                    // shadow: true,
                    // tooltip: {
                    //     valueDecimals: 2,//what is it mean?
                    // }
                }]
        }, function(chart) {
            // apply the date pickers
            setTimeout(function() {
                $('input.highcharts-range-selector', $('#' + chart.options.chart.renderTo))
                .datepicker({
//                showOtherMonths: true,
                dateFormat: "yy-mm-dd",
//                constrainInput: true,
//                maxDate:"+0d",
            })
            }, 0)
        });
    });


    // Set the datepicker's date format
//    $.datepicker.setDefaults({
//        dateFormat: 'yy-mm-dd',
//        onSelect: function(dateText) {
//            this.onchange();
//            this.onblur();
//        }
//    });

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
});


