/*
 * Common functions.
 */


function getTimezone() {
    // see https://stackoverflow.com/a/37512371
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

function fillTimezoneUIElements() {
    // inform the user
    var timezone = getTimezone();
    var timezoneInfo = document.getElementById("timezone-info");
    if (timezoneInfo) {
        timezoneInfo.innerText = timezone;
    }
    var select = document.getElementById("select-timezone");
    if (select) {
        var option = document.createElement("option");
        option.text = option.value = timezone;
        select.appendChild(option);
        configuration.timezones.forEach(function (timezone){
            var option = document.createElement("option");
            option.text = option.value = timezone;
            select.appendChild(option);
        });
        select.value = configuration.default_specification.timezone;
    }
}
