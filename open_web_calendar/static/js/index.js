// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only

/* This is used by the index/configuration page.
 *
 */

const EXAMPLE_SPECIFICATION = "https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/open_web_calendar/default_specification.yml";
const USER_PREFERRED_LANGUAGE = navigator.language.split("-")[0]; // credits to https://stackoverflow.com/a/3335420/1320237
const RAW_GITHUB_STATIC_URL = "https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/static"; // content served by the open web calendar and statically on github
const ENCRYPTION_PREFIX = "fernet://";

/* Encrypt a JSON value and return the response.
    {'token':'encrypt://...'}
*/
async function encryptJson(json) {
    // see https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    const url = "/encrypt";
    json.password = document.getElementById("encryption-password").value;
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}: ${response.text()}`);
    }
    return await response.json();
}

function canEncrypt(url) {
    return !urlIsEncrypted(url) && !RegExp(/^\s*$/).exec(url)
}


function updateUrls() {
    updateCalendarInputs();
    updateOutputs();
}

function updateCalendarInputs() {
    const urlInputs = document.getElementsByClassName("calendar-url-input");
    let calendar_index;
    for (calendar_index = 0; calendar_index < urlInputs.length; calendar_index+= 1) {
        const urlInput = urlInputs[calendar_index];
        const cssTemplate = ".CALENDAR-INDEX-" + calendar_index + ", .CALENDAR-INDEX-" + calendar_index + " .dhx_body, .CALENDAR-INDEX-" + calendar_index + " .dhx_title  { background-color: {color}; } \n";
        urlInput.owcColor.setAttribute("cssTemplate", cssTemplate);
        
    }
    const encryptButtons = document.getElementsByClassName("encrypt-button");
    for (const encryptButton of encryptButtons) {
        const url = encryptButton.link.owcGetUrl();
        encryptButton.innerText = urlIsEncrypted(url) ? 
            "🔒 " + translations["button-encrypted"] :
            "🔑 " + translations["button-encrypt"];
        encryptButton.disabled = !canEncrypt(url);
    }
}

function getUrls() {
    let urls = [];
    let urlInputs = document.getElementsByClassName("calendar-url-input");
    for (var i = 0; i < urlInputs.length; i+= 1) {
        let urlInput = urlInputs[i];
        let url = urlInput.owcGetUrl();
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


/* Create a mapping for the map.
 * If you add something here, also add it to the options in the index.html template.
 * Berlin, the capital city of Germany, has a latitude of 52.520008 and a longitude of 13.404954.
 * OpenStreetMap is the default, so make sure this is the same value as in the default_specification.yml.
 */

function getMapOptions() {
    return {
        "osm" : {
            // configuration.default_specification.event_url_location,
            "location": "https://www.openstreetmap.org/search?query={location}",
            // configuration.default_specification.event_url_geo,
            "geo": "https://www.openstreetmap.org/#map={zoom}/{lat}/{lon}",
        },
        "google" : {
            "location": "https://www.google.com/maps/search/{location}",
            "geo": "https://www.google.com/maps/@{lat},{lon},{zoom}z",
        },
        "bing" : {
            "location": "https://www.bing.com/maps?q={location}&lvl={zoom}",
            "geo": "https://www.bing.com/maps?brdr=1&cp={lat}%7E{lon}&lvl={zoom}",
        },
        "geo" : {
            "location": "",
            "geo": "geo:{lat},{lon}",
        },
        "none" : {
            "location": "",
            "geo": "",
        },
        "yandex" : {
            "location": "https://yandex.com/maps?text={location}",
            "geo": "https://yandex.com/maps/?ll={lon}%2C{lat}&z={zoom}",
        },
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
    } else {
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
    let checkbuttons = document.getElementsByClassName("specification-list-checkbox");
    for (let checkbutton of checkbuttons) {
        if (checkbutton.checked) {
            spec[checkbutton.classList[0]].push(checkbutton.value);
        }
    }
    /* event status */
    checkbuttons = document.getElementsByClassName("specification-checkbox");
    for (let checkbutton of checkbuttons) {
        spec[checkbutton.id] = checkbutton.checked;
    }
    /* map */
    const mapInputs = document.getElementById("select-map");
    const options = getMapOptions();
    const optionId = mapInputs.value;
    const option = options[optionId];
    if (option == null) {
        // We use the custom fields
        const inputGeo = document.getElementById("map-link-geo");
        spec.event_url_geo = inputGeo.value;
        const inputLocation = document.getElementById("map-link-location");
        spec.event_url_location = inputLocation.value;
    } else {
        spec.event_url_geo = option.geo;
        spec.event_url_location = option.location;
    }

    /**************** Set all specification values before this line ****************/
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
// allow downloads of ICS files: https://stackoverflow.com/a/64382081
var TARGET_TO_SANDBOX = {
  "_blank": 'sandbox="allow-scripts allow-same-origin allow-popups allow-downloads"',
  "_top": 'sandbox="allow-scripts allow-same-origin allow-top-navigation allow-downloads"',
  "_parent": 'sandbox="allow-scripts allow-same-origin allow-top-navigation allow-downloads"', // https://stackoverflow.com/a/16929749/1320237
  "_self": 'sandbox="allow-scripts allow-same-origin allow-downloads"' // https://stackoverflow.com/a/17802841/1320237
}

function getCalendarSourceCode(url, specification) {
    const calendar = document.getElementById("open-web-calendar");
    const height = calendar ? calendar.offsetHeight : 600;
    const code =
        '<iframe id="open-web-calendar" ' +
        (shouldShowAnimationForLoading() ?
        '\n    style="background:url(\'' + getLoadingAnimationUrl().replace(/'/g, "%27") + '\') center center no-repeat;"': "") +
        '\n    src="' + escapeHtml(url) + '"' +
        '\n    ' + TARGET_TO_SANDBOX[specification.target || configuration.default_specification.target] +
        '\n    allowTransparency="true" scrolling="no" ' +
        '\n    frameborder="0" height="' + height + 'px" width="100%"></iframe>';
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
    let element = document.createElement('a');
    element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function fillFirstInputWithData() {
    let defaultUrls = configuration.default_specification.url;
    for (let url of ((typeof specification.url) == "string" ? [specification.url] : specification.url)) {
        const link = addURLToList(url, arraysEqual(defaultUrls, specification.url));
    }
}

function fillMapInputs() {
    const mapInputs = document.getElementById("select-map");
    const lastChild = mapInputs.lastElementChild;
    const options = getMapOptions();
    var optionChosen = false;
    getOwnProperties(options).forEach(function (optionId) {
        /* select an option */
        const option = options[optionId];
        if (option.geo == specification.event_url_geo && option.location == specification.event_url_location) {
            mapInputs.value = optionId;
            optionChosen = true;
        }
    });
    if (!optionChosen) {
        mapInputs.value = "";
    }
    mapInputs.appendChild(lastChild);
    const inputGeo = document.getElementById("map-link-geo");
    inputGeo.value = specification.event_url_geo;
    const inputLocation = document.getElementById("map-link-location");
    inputLocation.value = specification.event_url_location;
    function onSelect() {
        const optionId = mapInputs.value;
        // see https://www.w3schools.com/jsref/prop_details_open.asp
        // open and close the details
        document.getElementById("map-details").open = optionId == "";
        const option = options[optionId];
        if (option) {
            inputGeo.value = option.geo;
            inputLocation.value = option.location;    
        }
        updateOutputs();
    };
    mapInputs.addEventListener("change", onSelect);
    mapInputs.addEventListener("keyup", onSelect);
    /* React to typing in the fields */
    function selectLastOption() {
        mapInputs.value = "";
        updateOutputs();
    }
//    inputGeo.addEventListener("change", selectLastOption);
    inputGeo.addEventListener("keyup", selectLastOption);
//    inputLocation.addEventListener("change", selectLastOption);
    inputLocation.addEventListener("keyup", selectLastOption);
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
    const select = document.getElementById("select-target");
    select.value = specification.target;
    select.onchange = updateOutputs;
}

function initializeCollectedCheckBoxes() {
  const checkboxes = document.getElementsByClassName("specification-checkbox");
  for (const checkbox of checkboxes) {
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
    const initialView = document.getElementById("select-tab");
    initialView.value = specification.tab;
    changeSpecificationOnChange(initialView);
    /* We update the checkbuttons according to the specification. */
    const specificationCheckbuttons = document.getElementsByClassName("specification-list-checkbox");
    const checkbuttons = {};
    for (const checkbutton of specificationCheckbuttons) {
        const list = checkbutton.classList[0];// The list we include the button in
        checkbutton.checked = specification[list].includes(checkbutton.value);
        checkbuttons[checkbutton.value] = checkbutton;
        changeSpecificationOnChange(checkbutton);
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
    fillMapInputs();
    updateCalendarInputs();
    updateControls();
    // updating what can be seen
    updateOutputs();
    fillDefaultSpecificationLink();
    fillPasswordField();
    listenForCalDavCalendars();
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

function togglePasswordVisibility(id) {
    const password = document.getElementById(id);
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}

function fillPasswordField() {
    const password = document.getElementById("encryption-password");
    // see https://stackoverflow.com/a/9719815/1320237
    password.value = Math.random().toString(36).slice(-8);
}

async function decrypt(token) {
    const url = "/decrypt";
    json = {
        "passwords": [document.getElementById("encryption-password").value],
        "token": token,
    }
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}: ${response.text()}`);
    }
    return await response.json();
}

function decryptURLs() {
    const password = document.getElementById("encryption-password").value;
    const urlInputs = document.getElementsByClassName("calendar-url-input");
    for (let urlLink of urlInputs) {
        const url = urlLink.owcGetUrl();
        if (urlIsEncrypted(url)) {
            decrypt(url, password).then(function(result) {
                urlLink.owcSetUrl(result.data.url);
                updateUrls();
            });
        }
    }
}

function toggleUrlCredentials(){
    const data = getURLFromInput();
    fillInUrlEditFields(data.url, !data.isPublic || urlIsEncrypted(data.url));
    return false;
}

function fillInUrlEditFields(url, isPublic) {
    const addUrls = document.getElementById("add-url-paragraph");
    const credentialsCheckbox = document.getElementById("add-url-credentials-checkbox");
    credentialsCheckbox.checked = isPublic;
    if (isPublic) {
        addUrls.classList.remove("toggle-default-visibility");
    } else {
        addUrls.classList.add("toggle-default-visibility");
    }
    const urlInput = document.getElementById("add-url-url");
    const passwordInput = document.getElementById("add-url-password");
    const usernameInput = document.getElementById("add-url-username");
    let urlObject;
    try {
        urlObject = new URL(url);
    } catch (error) {
        urlInput.value  = url;
        return;
    }
    if (isPublic) {
        urlInput.value = urlObject.href;
        passwordInput.value = "";
        usernameInput.value = "";
    } else {
        passwordInput.value = urlObject.password;
        usernameInput.value = urlObject.username;
        urlObject.password = urlObject.username = "";
        urlInput.value = urlObject.href;
    }
    updateCalDavCoice();
}

function getURLFromInput() {
    const userUrl = document.getElementById("add-url-url").value;
    const isPublic = isPublicUrlInUI() || urlIsEncrypted(userUrl);
    let url = userUrl;
    let urlObject
    try {
        urlObject = new URL(userUrl);
    } catch (error) {
        url = "https://" + userUrl;
        try {
            urlObject = new URL(url);
        } catch (error) {
            return {
                url: userUrl,
                isPublic: isPublic,
                "username": "",
                "password": "",
                "withoutCredentials": userUrl
            }
        }
    }
    username = document.getElementById("add-url-username").value || urlObject.username;
    password = document.getElementById("add-url-password").value || urlObject.password;
    urlObject.username = username;
    urlObject.password = password;
    url = urlObject.href;
    const withoutCredentials = new URL(url);
    withoutCredentials.username = withoutCredentials.password = "";
    return {
        "url": url,
        "isPublic": isPublic,
        "username": username,
        "password": password,
        "withoutCredentials": withoutCredentials.href,
    }
}

function getUrlFromCalDAVSelection() {
    const calendarSelect = document.getElementById("add-url-calendars");
    const enableSignUp = document.getElementById("caldav-enable-sign-up").checked;
    const urlOptions = enableSignUp ? "#can_add_email_attendee=true" : "";
    const url = calendarSelect.value + urlOptions;
    if (url) {
        return {
            "url": url,
            "isPublic": isPublicUrlInUI()
        }
    }
    return null;
}

function isPublicUrlInUI() {
    const addUrls = document.getElementById("add-url-paragraph");
    return !addUrls.classList.contains("toggle-default-visibility");
}

function addURLFromInput() {
    const url = getUrlFromCalDAVSelection() || getURLFromInput();
    if (!url.isPublic) {
        encryptJson({
            "url": url.url,
        }).then(function(result) {
            console.log(result);
            addURLToList(result.token);
        }).catch(function(error) {
            console.error(error);
            addURLToList(url.url);
        })
    } else {
            addURLToList(url.url);
    }
}

function addURLToList(url, isDefault) {
    removeDefaultCalendars();
    const li = document.createElement("li");
    /* input for urls */
    const link = document.createElement("a");
    link.classList.add("calendar-url-input");
    let currentUrl = url;
    link.owcSetUrl = function(url){
        currentUrl = url;
        link.innerText = url;
        link.href = url;
        updateUrls();
    }
    link.owcGetUrl = function() {
        return currentUrl;
    }
    link.target = "_blank";
    link.owcIsDefault = isDefault || false;
    li.appendChild(link);
    link.owcRemove = function() {
        calendarUrls.removeChild(li);
        updateUrls();
    }
    const color = link.owcColor = document.createElement("input");
    color.type = "color";
    color.classList.add("color-input");
    color.value = "#fefefe";
    color.addEventListener("change", updateUrls);
    color.addEventListener("keyup", updateUrls);
    li.appendChild(color);
    /* Encrypt and decrypt urls */
    const encryptButton = document.createElement("button");
    encryptButton.innerText = translations["button-encrypt"];
    encryptButton.classList.add("encrypt-button");
    encryptButton.classList.add("encryption-required");
    encryptButton.link = link;
    encryptButton.addEventListener("click", function() {
        const url = link.owcGetUrl();
        if (canEncrypt(url)) {
            /* not encrypted */
            encryptJson({
                "url": url
            }).then(function(response) {
                link.owcSetUrl(response["token"]);
            });
        }
    });
    li.appendChild(encryptButton);
    const editButton = document.createElement("button");
    editButton.innerText = "✏️ " + translations["button-edit"];
    editButton.onclick = function() {
        editUrl(link.owcGetUrl());
    }
    li.appendChild(editButton);
    const removeButton = document.createElement("button");
    removeButton.innerText = "❌ " + translations["button-remove"];
    removeButton.onclick = link.owcRemove;
    if (!isDefault) {
        li.appendChild(removeButton);
    }
    const calendarUrls = document.getElementById("calendar-urls");
    calendarUrls.appendChild(li);
    // last before return 
    link.owcSetUrl(url);
    return link;
}

function removeDefaultCalendars() {
    const calendarUrls = document.getElementById("calendar-urls");
    calendarUrls.querySelectorAll(".calendar-url-input").forEach(function(urlLink) {
        if (urlLink.owcIsDefault) {
            urlLink.owcRemove()
        }
    });
}

function listenForCalDavCalendars() {
    [
        document.getElementById("add-url-url"),
        document.getElementById("add-url-username"),
        document.getElementById("add-url-password"),
    ].forEach(function(input) {
        input.addEventListener("change", deferCall(updateCalDavCoice));
        input.addEventListener("keyup", deferCall(updateCalDavCoice));
        });
}

async function getCalDavCalendars() {
    const json = getURLFromInput();
    // see https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    const url = "/caldav/list-calendars";
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}: ${response.text()}`);
    }
    return await response.json();
}

function updateCalDavCoice() {
    const caldavOptions = document.getElementById("caldav-options");
    const calendarSelect = document.getElementById("add-url-calendars");
    const currentUrl = getURLFromInput();
    getCalDavCalendars().then(function(calendars) {
        calendarSelect.innerHTML = "";
        console.log("calendars", calendars);
        calendars.calendars.forEach(function(calendar) {
            const option = document.createElement("option");
            option.value = calendar.url;
            const calendarName = calendar.url.match(RegExp("/[^/]+/?$"));
            option.innerText = calendar.name;
            calendarSelect.appendChild(option);
            if (calendarName && currentUrl.url.includes(calendarName[0])) {
                calendarSelect.value = calendar.url;
            }
        });
        if (calendars.length == 0) {
            caldavOptions.classList.remove("visible");
        } else {
            caldavOptions.classList.add("visible");
        }
    }, function(error) {
        caldavOptions.classList.remove("visible");
        calendarSelect.innerHTML = "";
        console.error(error);
    });
}

function editUrl(url) {
    const password = document.getElementById("encryption-password").value;
    if (urlIsEncrypted(url)) {
        decrypt(url, password).then(function(result) {
            fillInUrlEditFields(result.data.url, false);
        }).catch(function(error) {
            console.error(error);
            fillInUrlEditFields(url, true);
        });
    } else {
        fillInUrlEditFields(url, true);
    }
}

function urlIsEncrypted(url) {
    return url.startsWith(ENCRYPTION_PREFIX);
}

const function2timeout = {};
const CALL_MS_AFTER_INPUT = 100;

/* We want to defer calling a function if it is called a lot of times like by typing into a text field. */
function deferCall(callback) {
    function wrapper(...args) {
        let timeoutId = function2timeout[callback];
        if (timeoutId) {
            try {
                clearTimeout(timeoutId);
            } catch (e) {
                // the timeout was cancelled.
            }
            delete function2timeout[callback];
        }
        function2timeout[callback] = setTimeout(function() {
            callback(...args);
            delete function2timeout[callback];
        }, CALL_MS_AFTER_INPUT);
    }
    return wrapper;
}
