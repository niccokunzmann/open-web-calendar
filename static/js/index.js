
const DEFAULT_URL = document.location.protocol + "//" + document.location.host;

function updateUrls() {
    updateCalendarInputs();
    updateOutputs();
}

function updateCalendarInputs() {
    var urlInputs = document.getElementsByClassName("calendar-url-input");
    var calendarUrls = document.getElementById("calendar-urls");
    var hasEmptyInput = false;
    for (var i = 0; i < urlInputs.length; i+= 1) {
        var urlInput = urlInputs[i];
        hasEmptyInput |= urlInput.value == "";
    }
    if (!hasEmptyInput) {
        var li = document.createElement("li");
        var input = document.createElement("input");
        input.type = "text";
        input.classList.add("calendar-url-input");
        input.addEventListener("change", updateUrls);
        input.addEventListener("keyup", updateUrls);
        input.id = "calendar-url-input-" + urlInputs.length;
        li.appendChild(input);
        calendarUrls.appendChild(li);
    }
}

function getUrls() {
    var urls = [];
    var urlInputs = document.getElementsByClassName("calendar-url-input");
    for (var i = 0; i < urlInputs.length; i+= 1) {
        var urlInput = urlInputs[i];
        var url = urlInput.value;
        if (url) {
            urls.push(url);
        }
    }
    return urls;
}

function getCalendarUrl(urls) {
    var url;
    if (document.location.protocol == "file:") {
        url =  + "/join-calendars.ics?";
    } else {
        url = DEFAULT_URL + "/calendar.html?";
    }
    var arguments = urls.map(function(url){
        return "url=" + encodeURIComponent(url)
    });
    return url + arguments.join("&");
}

var lastCalendarUrl = "";

function updateOutputs() {
    var urls = getUrls();
    console.log("urls", urls);
    var calendarUrl = getCalendarUrl(urls);
    if (lastCalendarUrl == calendarUrl) {
        return;
    }
    lastCalendarUrl = calendarUrl;
    console.log("calendarUrl", calendarUrl);
    displayCalendarLink(calendarUrl);
    displayCalendar(calendarUrl);
    showCalendarSourceCode(calendarUrl);
    
}

function displayCalendarLink(url) {
    var link = document.getElementById("calendar-link");
    link.innerText = url;
    link.href = url;
}
function displayCalendar(url) {
    var link = document.getElementById("open-web-calendar");
    link.src = url;
}
function showCalendarSourceCode(url) {
    var link = document.getElementById("calendar-code");
    link.innerText = '<iframe id="open-web-calendar" \n    src="' + encodeURIComponent(url) + '" \n    allowTransparency="true" scrolling="no" \n    frameborder="0" height="600px" width="100%"></iframe>'
}




window.addEventListener("load", function(){
    updateCalendarInputs();
});



