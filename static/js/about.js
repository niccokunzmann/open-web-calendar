// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only

function loadCalendarInDifferentTimeZone() {
    var timezoneSelect = document.getElementById("select-timezone");
    specification.timezone = timezoneSelect.value;
    document.location = getCalendarUrl(specification);
}


window.addEventListener("load", function(){
    // initialization
    fillTimezoneUIElements(specification.timezone || getTimezone());
});