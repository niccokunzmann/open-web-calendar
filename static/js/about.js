

function loadCalendarInDifferentTimeZone() {
    var timezoneSelect = document.getElementById("select-timezone");
    specification.timezone = timezoneSelect.value;
    document.location = getCalendarUrl(specification);
}


window.addEventListener("load", function(){
    // initialization
    fillTimezoneUIElements(specification.timezone || getTimezone());
});