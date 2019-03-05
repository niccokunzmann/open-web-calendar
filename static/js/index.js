
const DEFAULT_URL = document.location.protocol + "//" + document.location.host;
const CALENDAR_ENDPOINT = "/calendar.html";
const EXAMPLE_SPECIFICATION = "https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/default_specification.json";
const USER_PREFERRED_LANGUAGE = navigator.language.split("-")[0]; // credits to https://stackoverflow.com/a/3335420/1320237

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

function getCalendarUrl(specification) {
    var url = DEFAULT_URL + CALENDAR_ENDPOINT + "?";
    var parameters = [];
    getOwnProperties(specification).forEach(function(property) {
        if (specification[property]) {
            (Array.isArray(specification[property]) ? specification[property] : [specification[property]]
            ).forEach(function(url){
                parameters.push(encodeURIComponent(property) + "=" + encodeURIComponent("" + url))
            });
        }
    });
    return url + parameters.join("&");
}

var lastCalendarUrl = "";

/* This is called after the inputs changed.
 *
 */
function updateOutputs() {
    var specification = getSpecification();
    var calendarUrl = getCalendarUrl(specification);
    if (lastCalendarUrl != calendarUrl) {
        updateCalendarOutputs(calendarUrl, specification);
    }
    lastCalendarUrl = calendarUrl;
    updateSpecificationOutput(specification);
}

function updateCalendarOutputs(calendarUrl, specification) {
    console.log("calendarUrl", calendarUrl);
    displayCalendarLink(calendarUrl);
    var sourceCode = getCalendarSourceCode(calendarUrl, specification);
    displayCalendar(sourceCode);
    showCalendarSourceCode(sourceCode);
}

/* Update the output of the specification.
 *
 */
function updateSpecificationOutput(specification) {
    document.getElementById("json-specification").innerText = JSON.stringify(specification, null, 2);
}

function getValueById(id) {
    var element = document.getElementById(id);
    return element.value;
}

/* Set a value in the specification if the value does not equal
 * the default.
 */
function setSpecificationValueFromId(specification, key, id) {
  var value = getValueById(id);
  if (value != configuration.default_specification[key]) {
      specification[key] = value;
  }
}

/* This generates the specification of the calendar.
 *
 */
function getSpecification() {
    var specification = {};
    /* url */
    var urls = getUrls();
    if (urls.length == 1) {
        specification.url = urls[0];
    } else if (urls.length > 1) {
        specification.url = urls;
    }
    /* title */
    setSpecificationValueFromId(specification, "title", "calendar-title");
    /* language */
    setSpecificationValueFromId(specification, "language", "select-language");
    /* skin */
    setSpecificationValueFromId(specification, "skin", "select-skin");
    /* color and CSS */
    var css = configuration.default_specification.css;
    var colorInputs = document.getElementsByClassName("color-input");
    for (var i = 0; i < colorInputs.length; i++) {
        var colorInput = colorInputs[i];
        var color = colorInput.value;
        if (color) {
            css += colorInput.getAttribute("csstemplate").formatUnicorn({
                "color": color
            }) + "\n";
        }
    }
    var customCss = getValueById("css-input");
    if (!customCss.match(/^\s*$/) /* only white spaces */) {
      css += customCss;
    }
    if (css) {
        specification.css = css;
    }
    /* link targets */
    setSpecificationValueFromId(specification, "target", "select-target");
    console.log("getSpecification", specification);
    return specification;
}

function displayCalendarLink(url) {
    var link = document.getElementById("calendar-link");
    link.innerText = url;
    link.href = url;
}
function displayCalendar(sourceCode) {
    var container = document.getElementById("calendar-code-execution");
    container.innerHTML = sourceCode;
}
function showCalendarSourceCode(sourceCode) {
    var link = document.getElementById("calendar-code");
    link.innerText = sourceCode;
}

// see also https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe
// An iframe which has both allow-scripts and allow-same-origin for its sandbox attribute can remove its sandboxing.
var TARGET_TO_SANDBOX = {
  "_blank": 'sandbox="allow-scripts allow-same-origin allow-popups"',
  "_top": 'sandbox="allow-scripts allow-same-origin allow-top-navigation"',
  "_parent": 'sandbox="allow-scripts allow-same-origin allow-top-navigation"', // https://stackoverflow.com/a/16929749/1320237
  "_self": 'sandbox="allow-scripts allow-same-origin"' // https://stackoverflow.com/a/17802841/1320237
}

function getCalendarSourceCode(url, specification) {
  return '<iframe id="open-web-calendar" \n    src="' + escapeHtml(url) + '"' +
         '\n    ' + TARGET_TO_SANDBOX[specification.target || configuration.default_specification.target] +
         '\n    allowTransparency="true" scrolling="no" ' +
         '\n    frameborder="0" height="600px" width="100%"></iframe>';
}

function escapeHtml(unsafe) {
    // from https://stackoverflow.com/a/6234804/1320237
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

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

function downloadJSONSpecification() {
    var specification = getSpecification();
    var text = JSON.stringify(specification, null, 4);
    var filename = specification.title ?
        specification.title.replace(/\s/g, "-") + ".json" :
        "calendar-specification.json";
    downloadJSONAsFile(filename, text);
}

/* Download content with a file name.
 *
 */
function downloadJSONAsFile(filename, text) {
    // from https://stackoverflow.com/a/18197341/1320237
    var element = document.createElement('a');
    element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function fillFirstInputWithData() {
    var urlInputs = document.getElementsByClassName("calendar-url-input");
    if (urlInputs) {
        urlInputs[0].value = "http://www.officeholidays.com/ics/ics_country_noregion.php?tbl_country=Germany";
    }
}


function fillDefaultSpecificationLink() {
    var link = document.getElementById("example-specification-link");
    var url = DEFAULT_URL + CALENDAR_ENDPOINT + "?specification_url=" + EXAMPLE_SPECIFICATION;
    link.innerText = url;
    link.href = url;
}


function fillLanguageChoice() {
    // see
    var select = document.getElementById("select-language");
    var selected = false;
    configuration.dhtmlx.languages.forEach(function (language){
        var option = document.createElement("option");
        option.text = language[0];
        var code = option.value = language[2];
        if (code == USER_PREFERRED_LANGUAGE) {
            option.selected = true;
            selected = true;
        }
        select.appendChild(option);
    });
    if (!selected) {
        select.value = configuration.default_specification.language;
    }
    // change the specification if the language changes
    // see https://stackoverflow.com/a/7858323/1320237
    select.onchange = updateOutputs;
}

function initializeSkinChoice() {
    var select = document.getElementById("select-skin");
    select.value = configuration.default_specification.skin;
    select.onchange = updateOutputs;
}

function initializeTitle() {
    var input = document.getElementById("calendar-title");
    changeSpecificationOnChange(input);
}

/* general event input for specification changes */

function changeSpecificationOnChange(input) {
    input.addEventListener("change", updateOutputs);
    input.addEventListener("keyup", updateOutputs);
}

/* Color and CSS customization */
function listenForCSSChanges() {
    var colorInputs = document.getElementsByClassName("color-input");
    for (var i = 0; i < colorInputs.length; i++) {
        var input = colorInputs[i];
        changeSpecificationOnChange(input);
    }
    var CSSText = document.getElementById("css-input");
    changeSpecificationOnChange(CSSText);
}

function initializeLinkTargetChoice() {
    var select = document.getElementById("select-target");
    select.value = configuration.default_specification.target;
    select.onchange = updateOutputs;
}


window.addEventListener("load", function(){
    // initialization
    listenForCSSChanges();
    fillLanguageChoice();
    initializeSkinChoice();
    initializeTitle();
    initializeLinkTargetChoice();
    updateCalendarInputs();
    fillFirstInputWithData();
    updateCalendarInputs();
    // updating what can be seen
    updateOutputs();
    fillDefaultSpecificationLink();
});

String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
function () {
    // from https://stackoverflow.com/a/18234317
    "use strict";
    var str = this.toString();
    if (arguments.length) {
        var t = typeof arguments[0];
        var key;
        var args = ("string" === t || "number" === t) ?
            Array.prototype.slice.call(arguments)
            : arguments[0];

        for (key in args) {
            str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
        }
    }

    return str;
};
