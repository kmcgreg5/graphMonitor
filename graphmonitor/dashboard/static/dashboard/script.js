$(document).ready(function() {
    $('#datetimes').daterangepicker({
        timePicker: true,
        
        locale: {
          format: 'M/DD hh:mm A'
        }
    }, function() {console.log("Test");});

    $('#switchCurrentData').change(connectWebSocket);
});

function connectWebSocket() {
    if ($('#switchCurrentData').is(":checked") === true) {
        $('#datetimes').prop('disabled', true);
    } else {
        $('#datetimes').prop('disabled', false);
    }
}
    