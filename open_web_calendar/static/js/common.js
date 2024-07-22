// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only

/*
 * Common functions.
 */
const DEFAULT_URL = document.location.protocol + "//" + document.location.host;
const CALENDAR_ENDPOINT = "/calendar.html";
const CALENDAR_INFO_ENDPOINT = "/calendar.json";


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

function getCalendarUrl(specification, calendarEndpoint) {
    var url = DEFAULT_URL + (calendarEndpoint ? calendarEndpoint : CALENDAR_ENDPOINT) + "?";
    var parameters = [];
    getOwnProperties(specification).forEach(function(property) {
        (Array.isArray(specification[property]) ? specification[property].length ? specification[property] : [""] : [specification[property]]
        ).forEach(function(url){
            parameters.push(encodeURIComponent(property) + "=" + encodeURIComponent("" + url))
        });
    });
    return url + parameters.join("&");
}

/* Get the calendar information. */
function getCalendarInfo(onSuccess, spec) {
    var requestSpec = spec ? spec : specification;
    var endpoint = getCalendarUrl(requestSpec, CALENDAR_INFO_ENDPOINT);

    // from https://developer.mozilla.org/en-US/docs/Web/API/Request/json
    //const request = new Request(endpoint, {method: "GET"});  
    //console.log("GET " + endpoint);
    //return request;
    // from https://www.w3schools.com/js/js_json_http.asp
    var xmlhttp = new XMLHttpRequest();
    var url = endpoint;

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                var value = JSON.parse(this.responseText);
                onSuccess(value);
            } else {
                // TODO: report error
            }
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}
