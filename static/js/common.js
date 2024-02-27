/*
 * Common functions.
 */
const DEFAULT_URL = document.location.protocol + "//" + document.location.host;
const CALENDAR_ENDPOINT = "/calendar.html";


/* Return the properties of an object.
 *
 */
function getOwnProperties(object) {
    // from https://stackoverflow.com/a/16735184/1320237
    var ownProperties = [];
    for (var property in object) {
        if (object.hasOwnProperty(property)) {
            ownProperties.push(property);
        }
    }
    return ownProperties;
}

function shallowCopy(object) {
    var copy = {};
    for (let attribute of getOwnProperties(object)) {
      copy[attribute] = object[attribute];
    }
    return copy;
}

function getTimezone() {
    // see https://stackoverflow.com/a/37512371
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

function fillTimezoneUIElements(defaultTimeZone) {
    // inform the user
    var timezone = getTimezone();
    var timezoneInfo = document.getElementsByClassName("timezone-of-browser");
    for (var i = 0; i < timezoneInfo.length; i++) {
        timezoneInfo[i].innerText = timezone;
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
        select.value = defaultTimeZone;
    }
}

function getCalendarUrl(specification) {
    var url = DEFAULT_URL + CALENDAR_ENDPOINT + "?";
    var parameters = [];
    getOwnProperties(specification).forEach(function(property) {
        (Array.isArray(specification[property]) ? specification[property].length ? specification[property] : [""] : [specification[property]]
        ).forEach(function(url){
            parameters.push(encodeURIComponent(property) + "=" + encodeURIComponent("" + url))
        });
    });
    return url + parameters.join("&");
}
