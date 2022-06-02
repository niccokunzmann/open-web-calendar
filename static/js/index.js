/* This is used by the index/configuration page.
 *
 */

const DEFAULT_URL = document.location.protocol + "//" + document.location.host;
const CALENDAR_ENDPOINT = "/calendar.html";
const EXAMPLE_SPECIFICATION = "https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/default_specification.yml";
const USER_PREFERRED_LANGUAGE = navigator.language.split("-")[0]; // credits to https://stackoverflow.com/a/3335420/1320237
const RAW_GITHUB_STATIC_URL = "https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/static"; // content served by the open web calendar and statically on github


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
        (Array.isArray(specification[property]) ? specification[property] : [specification[property]]
        ).forEach(function(url){
            parameters.push(encodeURIComponent(property) + "=" + encodeURIComponent("" + url))
        });
    });
    return url + parameters.join("&");
}

/* This is called after the inputs changed.
 *
 */
function updateOutputs() {
    var specification = getSpecification();
    var calendarUrl = getCalendarUrl(specification);
    updateCalendarOutputs(calendarUrl, specification);
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
    /* starting date */
    setSpecificationValueFromId(specification, "starting_date", "starting-date");
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
    /* loader */
    setSpecificationValueFromId(specification, "loader", "select-loader");
    /* initial view */
    setSpecificationValueFromId(specification, "tab", "select-tab");
    /* controls */
    specification.controls = [];
    specification.tabs = [];
    var checkbuttons = document.getElementById("check-controls");
    for (var i = 0; i < checkbuttons.length; i++) {
        var checkbutton = checkbuttons[i];
        if (checkbutton.checked) {
            specification[checkbutton.classList[0]].push(checkbutton.value);
        }
    }
    ["tabs", "controls"].forEach(function(element){
        if (arraysEqual(specification[element], configuration.default_specification[element])) {
            delete specification[element];
            console.log("del;");
        }
    });
    /* print before exit */
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

function getLoadingAnimationUrl() {
    var url = getValueById("select-loader");
    if (url[0] == "/") {
        return RAW_GITHUB_STATIC_URL + url;
    }
    return url;
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
    var code =
        '<iframe id="open-web-calendar" ' +
        (shouldShowAnimationForLoading() ?
        '\n    style="background:url(\'' + getLoadingAnimationUrl().replace(/'/g, "%27") + '\') center center no-repeat;"': "") +
        '\n    src="' + escapeHtml(url) + '"' +
        '\n    ' + TARGET_TO_SANDBOX[specification.target || configuration.default_specification.target] +
        '\n    allowTransparency="true" scrolling="no" ' +
        '\n    frameborder="0" height="600px" width="100%"></iframe>';
    return code;
}

/* Whether the user should see an animation.
 * This is not in the specification as the server must be another server than
 * the one serving the calendar.
 */
function shouldShowAnimationForLoading() {
    return getLoadingAnimationUrl() != "";
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
        urlInputs[0].value = "https://www.calendarlabs.com/ical-calendar/ics/46/Germany_Holidays.ics";
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
    input.value = configuration.default_specification.title;
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

function initializeLoader() {
    var select = document.getElementById("select-loader");
    select.onchange = updateOutputs;
}

function updateLoader() {
    var defaultLoader = document.getElementById("default-loader");
    defaultLoader.value = configuration.default_specification.loader;
}

function updateControls() {
    var initialView = document.getElementById("select-tab");
    changeSpecificationOnChange(initialView);
    var form = document.getElementById("check-controls");
    var checkbuttons = {};
    ["tabs", "controls"].forEach(function(list) {
        var checkboxes = form.getElementsByClassName(list);
        var checked = configuration.default_specification[list];
        for (var i = 0; i < checkboxes.length; i++) {
            var checkbox = checkboxes[i];
            checkbox.checked = checked.includes(checkbox.value);
            checkbuttons[checkbox.value] = checkbox;
            changeSpecificationOnChange(checkbox);
        }
    });
    var labels = form.getElementsByTagName("label");
    for (var i = 0; i < labels.length; i++) {
        var label = labels[i];
        label.addEventListener("click", function(event) {
            var name = event.target.getAttribute("for");
            var checkbox = checkbuttons[name];
            checkbox.checked = !checkbox.checked;
            updateOutputs();
        });
    }
}

window.addEventListener("load", function(){
    // initialization
    listenForCSSChanges();
    fillLanguageChoice();
    initializeSkinChoice();
    initializeTitle();
    initializeLoader();
    initializeLinkTargetChoice();
    updateCalendarInputs();
    fillFirstInputWithData();
    updateCalendarInputs();
    updateLoader();
    updateControls();
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

function arraysEqual(a, b) {
  // from https://stackoverflow.com/a/16436975/1320237
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length != b.length) return false;
  for (var i = 0; i < a.length; ++i) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

