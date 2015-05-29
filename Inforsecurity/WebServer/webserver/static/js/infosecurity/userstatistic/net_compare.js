$(function() {
    var seriesOptions = [],
        yAxisOptions = [],
        seriesCounter = 0,
        names = $('#names').val(),
        colors = Highcharts.getOptions().colors;
        names = names.split(',');
        $.each(names, function(i, name) {
            //alert(name)
            $.getJSON('/ajax/userstatistic/get_net_compare_data?appprotc='+name, function(data) {
                
                datastr = '[' + data + ']'
                data_json = eval(datastr)
                //alert(data_json);
                seriesOptions[i] = {
                    name: name,
                    data: data_json
                };
                // As we're loading the data asynchronously, we don't know what order it will arrive. So
                // we keep a counter and create the chart when all the data is loaded.
                seriesCounter++;

                if (seriesCounter == names.length) {
                    createChart();
                }
            });
        });
    



    // create the chart when all data is loaded
    function createChart() {   

        // change it into chinese
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

        window.chart = new Highcharts.StockChart({
                    chart: {
                        renderTo: 'container_show',
                    },
                    rangeSelector: {
                        buttons: [{
                                type: 'all',
                                text: '全部',
                                count: 0
                            }, {
                                type: 'hour',
                                count: 60,
                                text: '1小时',
                            }, {
                                type: 'day',
                                count: 1,
                                text: '1天'
                            }],
                        selected: 0,
                    },
                    tooltip: 
                    {
                        xDateFormat:"%Y-%m-%d %H:%M:%S",
                        valueDecimals: 2
                    },
                    series: seriesOptions,
        });




    }

});