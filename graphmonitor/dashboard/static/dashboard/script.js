$(document).ready(function() {
    $('#datetimes').daterangepicker({
        timePicker: true,
        
        locale: {
          format: 'M/DD hh:mm A'
        }
    }, changeDateRange);

    $('#switchCurrentData').change(connectWebSocket);
    $('#selectModelBox').change(updateSelectionModalLink);

    let confirmationModal = $('#confirmationModal');
    confirmationModal.on('show.bs.modal', updateConfirmationModal);

    let selectionModal = $('#selectionModal');
    selectionModal.on('show.bs.modal', function(event) {
        let button = event.relatedTarget;
        let pk = button.getAttribute('data-bs-pk');
        $.get("/switch/" + pk + "/commands", updateSelectionModalOptions);
    });
});

function togglePolling(pk) {
    if ($("#switchPoll" + pk).is(":checked") === true) {
        startSwitch(pk);
    } else {
        stopSwitch(pk);
    }
}


function startSwitch(pk) {
    $.get("/switch/" + pk + "/start", function(data, status) {
        if (status == "success") {
            showMessage("Switch polling started.");
        } else {
            showMessage("Failed to start polling.");
        }
    });
}

function stopSwitch(pk) {
    $.get("/switch/" + pk + "/stop", function(data, status) {
        if (status == "success") {
            showMessage("Switch polling stopped.");
        } else {
            showMessage("Failed to stop polling.");
        }
    });
}

function showMessage(message) {
    let message_modal = $("#statusModal");
    let modal = bootstrap.Modal.getOrCreateInstance(message_modal);
    $("#statusModalBody").text(message);
    modal.show();
}

function updateConfirmationModal(event) {
    let button = event.relatedTarget;
    let type = button.getAttribute('data-bs-type');
    let pk = button.getAttribute('data-bs-pk');
    $("#confirmationModalButton").attr("onclick", "");
  
    if (type == "Switch") {
        $("#confirmationModalBody").text("Are you sure you want to delete this switch?");
        $("#confirmationModalButton").attr("onclick", "deleteSwitch(" + pk + ");");
    } else if (type == "Device") {
        $("#confirmationModalBody").text("Are you sure you want to delete this device?");
        $("#confirmationModalButton").attr("onclick", "deleteDevice(" + pk + ");");
    } else if (type == "DataPoints") {
        $("#confirmationModalBody").text("Are you sure you want to delete the selected data points?");
        $("#confirmationModalButton").attr("onclick", "deleteDataPoints(" + pk + ");");
    }
}

function deleteSwitch(pk) {
    $.get("/switch/" + pk + "/delete", refreshPage);
}

function deleteDevice(pk) {
    $.get("/device/" + pk + "/delete", refreshPage)
}

function deleteDataPoints(pk) {
    let start = $("#datetimes").data('daterangepicker').startDate;
    let end = $("#datetimes").data('daterangepicker').endDate;
    
    $.post("/device/" + pk + "/data/delete/", {csrfmiddlewaretoken:Cookies.get('csrftoken'), start:start.format("YYYY-MM-DD HH:mm"), end:end.format("YYYY-MM-DD HH:mm")}, refreshPage)
}

function refreshPage(data, status) {
    if (status == "success") {
        window.location.reload();
    }
}

function updateSelectionModalOptions(data, status) {
    let select_element = $("#selectModelBox");
    select_element.children().remove().end().append("<option value selected>---------</option>");
    $('#selectionModalLink').attr("href", "");
    
    for (const [key, value] of Object.entries(data['commands'])) {
        let opt = document.createElement('option');
        opt.value = value;
        opt.innerHTML = key;
        select_element.append(opt);
    }
}

function updateSelectionModalLink() {
    let value = $("#selectModelBox").val();
    if (value !== "") {
        $('#selectionModalLink').attr("href", "/command/" + value);
    } else {
        $('#selectionModalLink').attr("href", "");
    }
}

function changeDateRange(start, end) {
    $.post("/graphs/all/", {csrfmiddlewaretoken:Cookies.get('csrftoken'), start:start.format("YYYY-MM-DD HH:mm"), end:end.format("YYYY-MM-DD HH:mm")}, updateGraphs);
}

function updateGraphs(data, status) {
    let canvas_elements = $("canvas");
    for (let i=0; i < canvas_elements.length; i++) {
        const chart = Chart.getChart(canvas_elements[i].id);
        if (chart) {
            chart.destroy();
        }
    }

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

// Creates input output line graphs
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
    