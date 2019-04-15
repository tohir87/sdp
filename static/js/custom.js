$('.datepicker').datepicker({
    orientation: 'bottom',
    icons: {
        time: 'fa fa-clock-o',
        date: 'fa fa-calendar',
        up: 'fa fa-chevron-up',
        down: 'fa fa-chevron-down',
        previous: 'fa fa-chevron-left',
        next: 'fa fa-chevron-right',
        today: 'fa fa-crosshairs',
        clear: 'fa fa-trash'
    }
});

function getReport(startDate_, endDate_) {
    console.log(startDate_, endDate_);
    let url = "/api/get_temp_humid?start_date=" + startDate_ + "&end_date=" + endDate_;

    $.get(url, function (err, data) {
        console.log(err, data)
    });
}

$("#btn_filter").click(function () {
    var start_date = $("#start_date").val();
    var end_date = $("#end_date").val();

    getReport(start_date, end_date);

});

function plot(start_date_, end_date_) {
    let url = "/api/get_temp_humid?start_date=" + start_date_ + "&end_date=" + end_date_;
    console.log("Api Url:", url);

    $.get(url, function (data) {
        Highcharts.chart('container', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Temperature/Humidity Reading'
            },
            subtitle: {
                text: 'Source: Sensor Data'
            },
            xAxis: {
                categories: data.categories,
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'Percent'
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>:({point.y:,0:0.1f})<br/>',
                split: true
            },
            plotOptions: {
                area: {
                    stacking: 'percent',
                    lineColor: '#ffffff',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#ffffff'
                    }
                }
            },
            series: [{
                name: 'Temperature',
                data: data.temperature
            }, {
                name: 'Humidity',
                data: data.humidity
            }]
        });
    });

}


