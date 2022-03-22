$(document).ready(function() {
    $('#datetimes').daterangepicker({
        timePicker: true,
        
        locale: {
          format: 'M/DD hh:mm A'
        }
    }, changeDateRange);

    $('#switchCurrentData').change(connectWebSocket);

    //createGraph();
});

function changeDateRange(start, end) {
    console.log(start.format("YYYY-MM-DD hh:mm"));
    $.post("/graphs/all", {csrfmiddlewaretoken:Cookies.get('csrftoken'), start:start.format("YYYY-MM-DD HH:mm"), end:end.format("YYYY-MM-DD HH:mm")}, updateGraphs);
}

function updateGraphs(data, status) {
    for (const [key, info] of Object.entries(data)) {
        createGraph("chart" + key, info);
    }
}

function connectWebSocket() {
    if ($('#switchCurrentData').is(":checked") === true) {
        $('#datetimes').prop('disabled', true);
    } else {
        $('#datetimes').prop('disabled', false);
    }
}

function createGraph(id, info) {
    const ctx = document.getElementById(id).getContext('2d');
    const myChart = new Chart(ctx, {
        
        type: 'line',
        data: {datasets: [{label: "Input", data: info.in, backgroundColor: "rgba(0, 255, 0, .8)", borderColor: "rgba(0, 255, 0, .3)"}, {label: "Output", data: info.out, backgroundColor: "rgba(255, 0, 0, .8)", borderColor: "rgba(255, 0, 0, .3)"}]},
        
        options: {
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(item) {return item.formattedValue + " KBps";}
                    }
                },
                title: {
                    display: true,
                    text: info.title
                },
                zoom: {
                    zoom: {wheel: {enabled: true}, pinch: {enabled: true}, mode: 'x'},
                    pan: {enabled: true},
                    limits: {x: {min: info.start, max: info.end}, y: {min: 0}}
                }
            },
            scales: {
                x: {
                    type: 'time',
                    min: info.start,
                    max: info.end,
                    time: {
                        displayFormats: {
                            hour: "MMM DD HH:mm",
                            minute: "MMM DD HH:mm"
                        }
                    },
                },
                y: {
                    beginAtZero: true,
                    min: 0,
                    title: {
                        display: true,
                        text: "Rate (KBps)"
                    }
                }
            }
        }
    });
}
    