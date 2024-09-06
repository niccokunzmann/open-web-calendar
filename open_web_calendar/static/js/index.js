// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only

/* This is used by the index/configuration page.
 *
 */

const EXAMPLE_SPECIFICATION = "https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/open_web_calendar/default_specification.yml";
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
    var calendar_index;
    for (calendar_index = 0; calendar_index < urlInputs.length; calendar_index+= 1) {
        var urlInput = urlInputs[calendar_index];
        hasEmptyInput |= urlInput.value == "";
    }
    if (!hasEmptyInput) {
        var li = document.createElement("li");
        /* input for urls */
        var input = document.createElement("input");
        input.type = "text";
        input.classList.add("calendar-url-input");
        input.addEventListener("change", updateUrls);
        input.addEventListener("keyup", updateUrls);
        input.id = "calendar-url-input-" + urlInputs.length;
        li.appendChild(input);
        /* input for calendar color
        <input type="color" value="#fefefe"
               placeholder="black" class="color-input"
               cssTemplate=".dhx_after .dhx_month_body, .dhx_before .dhx_month_body, .dhx_after .dhx_month_head, .dhx_before .dhx_month_head { background-color: {color}; }">*/
        var color = document.createElement("input");
        color.type = "color";
        color.classList.add("color-input");
        color.value = "#fefefe";
        var cssTemplate = ".CALENDAR-INDEX-" + calendar_index + ", .CALENDAR-INDEX-" + calendar_index + " .dhx_body, .CALENDAR-INDEX-" + calendar_index + " .dhx_title  { background-color: {color}; } \n";
        color.setAttribute("cssTemplate", cssTemplate);
        color.addEventListener("change", updateUrls);
        color.addEventListener("keyup", updateUrls);
        li.appendChild(color);
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

/* This is called after the inputs changed.
 *
 */
function updateOutputs() {
    var specification = getSpecification();
    var calendarUrl = getCalendarUrl(specification);
    updateCalendarOutputs(calendarUrl, specification);
    lastCalendarUrl = calendarUrl;
    updateSpecificationOutput(specification);
    updateLanguageOutput(specification);
}

function updateCalendarOutputs(calendarUrl, specification) {
    console.log("calendarUrl", calendarUrl);
    displayCalendarLink(calendarUrl);
    var sourceCode = getCalendarSourceCode(calendarUrl, specification);
    displayCalendar(sourceCode);
    showCalendarSourceCode(sourceCode);
}

function updateLanguageOutput(specification) {
    var span = document.getElementById("language-chosen");
    var select = document.getElementById("select-language");
    span.innerText = select.options[select.selectedIndex].innerText;
    var sections = [
        document.getElementById("section_prefer_browser_language_true"),
        document.getElementById("section_prefer_browser_language_false"),
    ];
    if (specification.prefer_browser_language) {
        sections.reverse();
    }
    sections[0].appendChild(span);
    sections[1].appendChild(select);
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
    var spec = shallowCopy(specification);
    /* url */
    var urls = getUrls();
    if (urls.length == 1) {
        spec.url = urls[0];
    } else if (urls.length > 1) {
        spec.url = urls;
    }
    /* title */
    setSpecificationValueFromId(spec, "title", "calendar-title");
    /* starting date */
    setSpecificationValueFromId(spec, "date", "starting-date");
    /* starting hour */
    setSpecificationValueFromId(spec, "starting_hour", "starting-hour");
    /* ending hour */
    setSpecificationValueFromId(spec, "ending_hour", "ending-hour");

    /* time increment */
    let time_increment = document.getElementById("time-increment");
    for (let c of time_increment.getElementsByClassName("time-increment-input")) {
        if (c.checked && configuration.default_specification.hour_division != c.value) {
            spec.hour_division = c.value;
        }
    }

    /* hour format */
    setSpecificationValueFromId(spec, "hour_format", "select-hour-format");
    /* language */
    setSpecificationValueFromId(spec, "language", "select-language");
    spec.prefer_browser_language = document.getElementById("prefer_browser_language_true").checked;
    /* skin */
    setSpecificationValueFromId(spec, "skin", "select-skin");
    /* Start of the week */
    setSpecificationValueFromId(spec, "start_of_week", "select-start-of-week");
    /* timezone */
    setSpecificationValueFromId(spec, "timezone", "select-timezone");
    /* color and CSS */
    var css = configuration.default_specification.css;
    var colorInputs = document.getElementsByClassName("color-input");
    for (var i = 0; i < colorInputs.length; i++) {
        var colorInput = colorInputs[i];
        var color = colorInput.value;
        if (color && color != "#fefefe") {
            css += colorInput.getAttribute("csstemplate").formatUnicorn({
                "color": color
            });
        }
    }
    var customCss = getValueById("css-input");
    if (!customCss.match(/^\s*$/) /* only white spaces */) {
      /* Add the custom CSS to the start of the file to override values from
         chosen color dialogs. */
      css = customCss + (css ? "\n" + css : "");
    }
    if (css) {
        spec.css = css;
    }
    /* link targets */
    setSpecificationValueFromId(spec, "target", "select-target");
    /* loader */
    setSpecificationValueFromId(spec, "loader", "select-loader");
    /* initial view */
    setSpecificationValueFromId(spec, "tab", "select-tab");
    /* controls */
    spec.controls = [];
    spec.tabs = [];
    var checkbuttons = document.getElementById("check-controls");
    for (var i = 0; i < checkbuttons.length; i++) {
        var checkbutton = checkbuttons[i];
        if (checkbutton.checked) {
            spec[checkbutton.classList[0]].push(checkbutton.value);
        }
    }
    /* event status */
    checkbuttons = document.getElementsByClassName("collect-if-checked");
    for (var i = 0; i < checkbuttons.length; i++) {
        var checkbutton = checkbuttons[i];
        spec[checkbutton.id] = checkbutton.checked;
    }
    /* delete duplicate values */
    getOwnProperties(configuration.default_specification).forEach(function(element){
        if (arraysEqual(spec[element], configuration.default_specification[element])) {
            delete spec[element];
        }
    });
    /* print before exit */
    console.log("getSpecification", spec);
    return spec;
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
    for (let url of ((typeof specification.url) == "string" ? [specification.url] : specification.url)) {
      updateCalendarInputs();
      var urlInputs = document.getElementsByClassName("calendar-url-input");
      urlInputs[urlInputs.length - 1].value = url;
    }
}


function fillDefaultSpecificationLink() {
    var link = document.getElementById("example-specification-link");
    var url = DEFAULT_URL + CALENDAR_ENDPOINT + "?specification_url=" + EXAMPLE_SPECIFICATION;
    link.innerText = url;
    link.href = url;
}


function fillLanguageChoice() {
    var select = document.getElementById("select-language");
    var selected = false;
    var selected_language = configuration.default_specification.language == specification.language ? USER_PREFERRED_LANGUAGE : specification.language;
    configuration.dhtmlx.languages.forEach(function (language){
        var option = document.createElement("option");
        var code = option.value = language[1];
        option.text = language[0] + " (" + code + ")";
        if (code == selected_language) {
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
    /*  ------ browser selection ------  */
    var choices = [
        document.getElementById("prefer_browser_language_false"),
        document.getElementById("prefer_browser_language_true"),
    ];
    choice = choices[specification.prefer_browser_language ? 1 : 0];
    choice.checked = true;
    choices.forEach((e) => e.onchange = updateOutputs)
}

function fillTimezoneChoice() {
    fillTimezoneUIElements(specification.timezone)
    changeSpecificationOnChange(document.getElementById("select-timezone"));
}

function initializeSkinChoice() {
    var select = document.getElementById("select-skin");
    select.value = getSkin();
    select.onchange = updateOutputs;
}

function initializeTitle() {
    var input = document.getElementById("calendar-title");
    input.value = specification.title;
    changeSpecificationOnChange(input);
}

function initializeStartDate() {
    var input = document.getElementById("starting-date");
    input.value = specification.date;
    changeSpecificationOnChange(input);
}

function initializeFirstHour() {
    var input = document.getElementById("starting-hour");
    input.value = specification.starting_hour;
    changeSpecificationOnChange(input);
}

function initializeLastHour() {
    var input = document.getElementById("ending-hour");
    input.value = specification.ending_hour;
    changeSpecificationOnChange(input);
}

function initializeTimeIncrement() {
    var input = document.getElementById("time-increment");
    var increment = document.getElementById("time-" + specification.hour_division)
    if (increment) {
        increment.checked = "checked";
    }
    for (let c of input.getElementsByClassName("time-increment-input")) {
        changeSpecificationOnChange(c);
    }
}

function select_option_and_add_if_absent(select, value) {
  select.value = value;
  if (select.selectedIndex == -1) {
    var option = document.createElement("option");
    option.value = value;
    option.innerText = value;
    select.appendChild(option);
    select.value = value;
  }
}

function initializeHourFormat() {
    var input = document.getElementById("select-hour-format");
    select_option_and_add_if_absent(input, specification.hour_format);
    changeSpecificationOnChange(input);
}

function initializeStartOfWeek() {
    var input = document.getElementById("select-start-of-week");
    input.value = specification.start_of_week;
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
    CSSText.value = specification.css;
    changeSpecificationOnChange(CSSText);
}

function initializeLinkTargetChoice() {
    var select = document.getElementById("select-target");
    select.value = specification.target;
    select.onchange = updateOutputs;
}

function initializeCollectedCheckBoxes() {
  var checkboxes = document.getElementsByClassName("collect-if-checked");
  for (var i = 0; i < checkboxes.length; i++) {
      var checkbox = checkboxes[i];
      changeSpecificationOnChange(checkbox);
      checkbox.checked = ["true", true, "yes"].includes(specification[checkbox.id]);
  }
}

function initializeLoader() {
    var defaultLoader = document.getElementById("default-loader");
    defaultLoader.value = configuration.default_specification.loader;
    var select = document.getElementById("select-loader");
    select_option_and_add_if_absent(select, specification.loader);
    select.onchange = updateOutputs;
}

function updateControls() {
    var initialView = document.getElementById("select-tab");
    initialView.value = specification.tab;
    changeSpecificationOnChange(initialView);
    var form = document.getElementById("check-controls");
    var checkbuttons = {};
    ["tabs", "controls"].forEach(function(list) {
        var checkboxes = form.getElementsByClassName(list);
        var checked = specification[list];
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
    fillTimezoneChoice();
    initializeStartOfWeek();
    initializeSkinChoice();
    initializeTitle();
    initializeStartDate();
    initializeFirstHour();
    initializeLastHour();
    initializeTimeIncrement();
    initializeHourFormat();
    initializeLoader();
    initializeCollectedCheckBoxes();
    initializeLinkTargetChoice();
    updateCalendarInputs();
    fillFirstInputWithData();
    updateCalendarInputs();
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
  if (typeof a != 'object') return a == b;
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length != b.length) return false;
  for (var i = 0; i < a.length; ++i) {
    if (!arraysEqual(a[i], b[i])) return false;
  }
  return true;
}
