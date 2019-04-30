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

$('a.delete_item').click(function () {
    console.log("im responding...")
    ask = confirm("Are you sure you want to delete the selection?(Y/N)")
    if (ask) {
        console.log("Going ahead with deletion")
        // self.location = 
    }
});

$('a.confirm_delete').click(function (e) {
    e.preventDefault();
    var url = this.href;
    var msg_ = $(this).data('msg');
    var title_ = $(this).data('title');

    console.log(url);

    swal({
        title: typeof title_ !== 'undefined' ? title_ : 'Are you sure?',
        text: typeof msg_ !== 'undefined' ? msg_ : "Are you sure you want to delete the selected item?",
        icon: 'warning',
        buttons: {
            cancel: {
                text: 'No, cancel',
                value: null,
                visible: true,
                className: "",
                closeModal: false
            },
            confirm: {
                text: 'Yes, go ahead!',
                value: true,
                visible: true,
                className: "bg-danger",
                closeModal: false
            }
        }
    }).then(function (isConfirm) {
        if (isConfirm) {
            self.location = url;
        } else {
            swal('Cancelled', 'Operation has been cancelled.', 'error');
        }
    });

});

function getReport(startDate_, endDate_) {
    console.log(startDate_, endDate_);
    let url = "/api/get_temp_humid?start_date=" + startDate_ + "&end_date=" + endDate_;

    $.get(url, function (data, status) {
        console.log(data, status);
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

$("#btn_filter").click(function () {
    var start_date = $("#start_date").val();
    var end_date = $("#end_date").val();

    getReport(start_date, end_date);

});

function plot(start_date_, end_date_) {
    let url = "/api/get_temp_humid?start_date=" + start_date_ + "&end_date=" + end_date_;
    console.log("Api Url:", url);

    $.get(url, function (data) {
        console.log(data.temperature);


    });

}


