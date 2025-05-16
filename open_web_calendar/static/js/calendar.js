// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only

/* This is used by the dhtmlx scheduler.
 *
 */

function parseDate(yyyy_mm_dd) {
    // parse a date without timezone information
    // see https://stackoverflow.com/questions/17545708/parse-date-without-timezone-javascript
    const numbers = yyyy_mm_dd.match(/(\d+)-0?(\d+)-0?(\d+)/)
    return new Date(parseInt(numbers[1]), parseInt(numbers[2]) - 1, parseInt(numbers[3]))
}

function escapeHtml(unsafe) {
    // from https://stackoverflow.com/a/6234804
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

function getQueries() {
    // from http://stackoverflow.com/a/1099670/1320237
    let qs = document.location.search;
    let tokens, re = /[?&]?([^=]+)=([^&]*)/g;
    qs = qs.split("+").join(" ");

    const queries = {};
    while (tokens = re.exec(qs)) {
        const id = decodeURIComponent(tokens[1]);
        const content = decodeURIComponent(tokens[2]);
        if (Array.isArray(queries[id])) {
            queries[id].push(content);
        } else if (queries[id]) {
            queries[id] = [queries[id], content];
        } else {
            queries[id] = content;
        }
    }
    return queries;
}

function isSafeUrl(urlString) {
    return !UNSAFE_URL_PROTOCOLS.some(function(protocol) {
        return urlString.toLowerCase().startsWith(protocol.toLowerCase() + ":");
    });
}

/* Create a link around the HTML text.
 * Use this instead of creating links manually because it also sets the
 * target according to the specification.
 */
function makeLink(url, html) {
    const link = document.createElement("a");
    link.target = specification.target;
    link.href = isSafeUrl(url) ? url : "#";
    link.innerHTML = html ? html : "";
    return link.outerHTML;
}


/*
 * Download the vent ICS with a file name.
 */
function downloadICS(event) {
    // from https://stackoverflow.com/a/18197341/1320237
    const element = document.createElement('a');
    const convert = scheduler.date.date_to_str("%Y-%m-%d %H%i", false);
    const filename = convert(event.start_date).replace(" 0000", "") +
    " " + event.text.replace(/[/:\\]/g, "-") + ".ics";
    let url = document.location.href.replace("/calendar.html", "/calendar.ics") + 
        "&filename=" + encodeURIComponent(filename) + 
        "&set_event=" + encodeURIComponent(event.ical);
    element.setAttribute('href', url);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    element.target = "_blank";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/*
 * Check whether a Date is located at the start of a day.
 */
function isStartOfDay(date) {
    return date.getHours() == 0 && date.getMinutes() == 0 && date.getSeconds() == 0;
}

/*
 * Check if the start and end are one day.
 */
function isOneDay(start, end) {
  return isStartOfDay(start) && isStartOfDay(end) && end - start == 24 * 60 * 60 * 1000;
}

// from https://stackoverflow.com/a/10262019/1320237
const isWhitespaceString = str => !str.replace(/\s/g, '').length;
const isNotWhitespaceString = str => !isWhitespaceString(str);

/*
 * join lines as HTML.
 * Ignore empty lines.
 */
function joinHtmlLines(lines) {
    return lines.filter(isNotWhitespaceString).join("<br/>")
}

/*
 * These are template functions to compose event details.
 * Use these instead of custom edits in the scheduler.template replacements.
 */
const template = {
    "plain_summary": function(event) {
        return escapeHtml(event.text);
    },
    "formatted_summary": function(event) {
      let summary = template.plain_summary(event);
      if (event.url) {
        summary = makeLink(event.url, "🔗 " + summary);
      }
      return summary;
    },
    "details": function(event) {
        const details = document.createElement("div");
        details.classList.add("details");
        details.innerHTML = event.description;
        // set the target of all the links
        const links = details.getElementsByTagName("a");
        for (const link of links) {
          link.target = specification.target;
        }
        return details.outerHTML;
    },
    "location": function(event) {
        if (!event.location) {
            return "";
        }
        return makeLink(event.location.url, escapeHtml(event.location.text || "🗺"));
    },
    "debug": function(event) {
        return "<pre class='debug' style='display:none'>" +
            escapeHtml(JSON.stringify(event, null, 2)) +
            "</pre>"
    },
    "categories": function (event) {
      if (event.categories.length) {
          return '<b class="categories">| ' + event.categories.map(escapeHtml).join(" | ") + ' |</b> ';
      }
      return "";
    },
    "date": function (start, end) {
        /* One day
         * Multiday
         * Within a day
         * From one day to another
         */
        if (isOneDay(start, end)) {
          return "";
        }
        return scheduler.templates.event_date(start) + " - " + scheduler.templates.event_date(end)
    },
    "participants" : function (participants) {
        if (!specification.show_organizers && !specification.show_attendees || participants.length == 0) {
            return "";
        }
        const details = document.createElement("details");
        details.classList.add("participants");
        const summary = document.createElement("summary");
        summary.innerText = OWCLocale.labels.participants;
        details.appendChild(summary);
        const ol = document.createElement("ol");
        for (const participant of participants) {
            if ((participant.is_oragnizer && !specification.show_organizers) ||
                (!participant.is_oragnizer && !specification.show_attendees)
            ) {
                continue;
            }
            const li = document.createElement("li");
            const link = makeLink("mailto:" + participant.email, escapeHtml(participant.name ? participant.name : participant.email));
            li.innerHTML = 
                '<div class="icon status"></div><div class="icon type"></div><div class="icon role"></div>' + 
                link;
            participant.css.forEach((e) => li.classList.add(e));
            ol.appendChild(li);
        }
        details.appendChild(ol);
        return details.outerHTML;
    }
}

function showError(element) {
    const icon = document.getElementById("errorStatusIcon");
    icon.classList.add("onError");
    const errors = document.getElementById("errorWindow");
    element.classList.add("item");
    errors.appendChild(element);
}

function toggleErrorWindow() {
    // const scheduler_tag = document.getElementById("scheduler_here");
    const errors = document.getElementById("errorWindow");
    // scheduler_tag.classList.toggle("hidden");
    errors.classList.toggle("hidden");
}

function showErrorWindows() {
    const errors = document.getElementById("errorWindow");
    errors.classList.remove("hidden");
}

function showXHRError(xhr) {
    const iframe = document.createElement("iframe");
    iframe.srcdoc = xhr.responseText;
    iframe.className = "errorFrame";
    showError(iframe);
}

function showEventError(error) {
    // show an error created by app.py -> error_to_dhtmlx
    const div = document.createElement("div");
    // HEADING
    const heading = document.createElement("h1");
    heading.innerText = error.text;
    div.appendChild(heading);
    // LINK
    const link = makeLink(error.url, escapeHtml(error.url));
    div.innerHTML += link;
    // DESCRIPTION
    const description = document.createElement("p");
    description.innerText = error.description;
    div.appendChild(description);
    // TRACEBACK
    const traceback = document.createElement("pre");
    traceback.innerText = error.traceback;
    div.appendChild(traceback);
    showError(div);
}

function showLoader() {
    let loader = document.getElementById("loader");
    loader.classList.remove("hidden");
}

function disableLoader() {
    let loader = document.getElementById("loader");
    loader.classList.add("hidden");
}

function setLoader() {
    if (specification.loader) {
        let loader = document.getElementById("loader");
        let url = specification.loader.replace(/'/g, "%27");
        loader.style.cssText += "background:url('" + url + "') center center no-repeat;"
    } else {
        disableLoader();
    }
}

function getHeader() {
    // elements that do not occur in the list will always be permitted
    const useHeaderElement = {
      "prev": specification.controls.includes("previous") ,
      "date": specification.controls.includes("date"),
      "next": specification.controls.includes("next"),
      "day": specification.tabs.includes("day"),
      "week": specification.tabs.includes("week"),
      "month": specification.tabs.includes("month"),
      "today": specification.controls.includes("today"),
      "agenda": specification.tabs.includes("agenda"),
      "menu": specification.controls.includes("menu"),
    }
    function showSelected(headerElements) {
      return headerElements.filter(function(element){
        return useHeaderElement[element.id || element] != false; // null for absent
      });
    }
    const menu = {
        id: "menu",
        /* the HTML for the menu is from here:
         * 6. Snappy Sliding Hamburger Menu - https://alvarotrigo.com/blog/hamburger-menu-css/
         * See also https://docs.dhtmlx.com/scheduler/api__scheduler_header_config.html
         */
        html:
            '<div class="hamburger-menu">' + 
                '<input id="menu__toggle__2" type="checkbox" class="menu__toggle"/>' +
                '<label class="menu__btn burger-menu-label" for="menu__toggle" id="burger-menu-label">' +
                    '<span></span>' +
                '</label>' +
            '</div>',
        css: "owc_nav_burger_menu" // the CSS class
    }
    // switch the header to a compact one
    // see https://docs.dhtmlx.com/scheduler/touch_support.html
    if (window.innerWidth < Number.parseInt(specification.compact_layout_width)) {
        return {
            rows: [
                {
                    cols: showSelected([
                        menu,
                        "prev",
                        "date",
                        "next",
                    ])
                },
                {
                    cols: showSelected([
                        "day",
                        "week",
                        "month",
                        "agenda",
                        "spacer",
                        "today"
                    ])
                }
            ]
          };
    } else {
        return showSelected([
            menu,
            "day",
            "week",
            "month",
            "agenda",
            "date",
            "prev",
            "today",
            "next"
        ]);
    }
}

function resetConfig() {
    scheduler.config.header = getHeader();
    return true;
}

// If you add an action XXX here, also add icon_XXX to the calendar translations
// And also an icon to static/img/icons/XXX.svg
const actions = {
    "subscribe": function(event) {
        console.log("Save event.", event);
        downloadICS(event);
    },
    "signup": (event) => {
        console.log("Sign up to event:", event);
        openSignUp(event);
    }
}

/* Disable/Enable features based on touch/mouse-over gestures
 * see https://stackoverflow.com/a/52855084/1320237
 */
const IS_TOUCH_SCREEN = window.matchMedia("(pointer: coarse)").matches;
const CAN_HAVE_TOOLTIP = !IS_TOUCH_SCREEN;


function loadCalendar() {
    /* Format the time of the hour.
     * see https://docs.dhtmlx.com/scheduler/settings_format.html
     * see https://docs.dhtmlx.com/scheduler/api__scheduler_hour_date_config.html
     */
    scheduler.config.hour_date = specification["hour_format"];
    const format = scheduler.date.date_to_str(scheduler.config.hour_date);

    // set the locale
    // loaded from /locale_<lang>.js
    // see also https://docs.dhtmlx.com/scheduler/api__scheduler_locale_other.html
    scheduler.i18n.setLocale(OWCLocale);
    // load plugins, see https://docs.dhtmlx.com/scheduler/migration_from_older_version.html#5360
    scheduler.plugins({
        agenda_view: true,
        multisource: true,
        quick_info: specification.plugin_event_details,
        recurring: false,
        tooltip: CAN_HAVE_TOOLTIP && specification.plugin_event_tooltip,
        readonly: true,
        limit: true,
        serialize: true,
    });
    // set format of dates in the data source
    scheduler.config.xml_date="%Y-%m-%d %H:%i";

    // responsive lightbox, see https://docs.dhtmlx.com/scheduler/touch_support.html
    scheduler.config.responsive_lightbox = true;
    resetConfig();
    scheduler.attachEvent("onBeforeViewChange", resetConfig);
    scheduler.attachEvent("onSchedulerResize", resetConfig);

    // set the skin, scheduler v7
    // see https://docs.dhtmlx.com/scheduler/skins.html#dark
    scheduler.setSkin(getSkin());
    /* Hide or display the header controls */
    if (!specification.controls.length && !specification.tabs.length) {
        document.body.classList.add("no-controls");
    } else {
        document.body.classList.remove("no-controls");
    }

    // we do not allow changes to the source calendar
    scheduler.config.readonly = true;
    /* Add a red line at the current time.
     * see https://docs.dhtmlx.com/scheduler/api__scheduler_hour_date_config.html
     * see https://docs.dhtmlx.com/scheduler/limits.html
     */
    scheduler.config.mark_now = true;
    // set the start of the week. See https://docs.dhtmlx.com/scheduler/api__scheduler_start_on_monday_config.html
    scheduler.config.start_on_monday = specification["start_of_week"] != "su";
    let hour_division = parseInt(specification["hour_division"]);
    scheduler.config.hour_size_px = 44 * hour_division;
    scheduler.templates.hour_scale = function(date){
    	const step = 60 / hour_division;
    	let html = "";
    	for (let i=0; i<hour_division; i++){
    	    html += "<div style='height:44px;line-height:44px;'>"+format(date)+"</div>"; // TODO: This should be in CSS.
    	    date = scheduler.date.add(date, step, "minute");
    	}
    	return html;
    }
    scheduler.config.first_hour = parseInt(specification["starting_hour"]);
    scheduler.config.last_hour = parseInt(specification["ending_hour"]);
    const date = specification["date"] ? parseDate(specification["date"]) : new Date();
    scheduler.init('scheduler_here', date, specification["tab"]);

    // see https://docs.dhtmlx.com/scheduler/custom_events_content.html
    // see https://docs.dhtmlx.com/scheduler/api__scheduler_event_bar_text_template.html
    scheduler.templates.event_bar_text = function(start, end, event){
        return template.plain_summary(event);
    }
/*    scheduler.templates.event_bar_date = function(start, end, event){
      console.log("event_bar_date");
      return template.date(start, end) + template.categories(event);
    }*/
    // see https://docs.dhtmlx.com/scheduler/custom_events_content.html
    scheduler.templates.event_header = function(start, end, event){
        return joinHtmlLines([template.date(start, end), template.categories(event)]);
    };


    // tooltip
    // see https://docs.dhtmlx.com/scheduler/tooltips.html
    if (CAN_HAVE_TOOLTIP) {
        scheduler.templates.tooltip_text = function(start, end, event) {
            return template.formatted_summary(event) + template.details(event) + template.location(event);
        };
        scheduler.config.tooltip_offset_x = 1;
        scheduler.config.tooltip_offset_y = 1;
    }
    // quick info
    // see https://docs.dhtmlx.com/scheduler/extensions_list.html#quickinfo
    scheduler.templates.quick_info_title = function(start, end, event){
        return template.formatted_summary(event);
    }
    scheduler.templates.quick_info_content = function(start, end, event){
        return template.details(event) +
            template.location(event) +
            template.participants(event.participants) +
            template.debug(event);
    }
    // see https://docs.dhtmlx.com/scheduler/api__scheduler_quick_info_date_template.html
    scheduler.templates.quick_info_date = function(start, end, event){
        return joinHtmlLines([template.date(start, end), template.categories(event)]);
    }

    // hide the button to sign up
    // see https://docs.dhtmlx.com/scheduler/api__scheduler_onquickinfo_event.html
    scheduler.attachEvent("onQuickInfo",function(eventId){
        const event = scheduler.getEvent(eventId);
        if (event.owc["X-OWC-CAN-ADD-ATTENDEE"] == "true") {
            document.body.classList.remove("cannot-sign-up");
        } else {
            document.body.classList.add("cannot-sign-up");
        }
    });

    // general style
    scheduler.templates.event_class=function(start,end,event){
        if (event.type == "error") {
            showEventError(event);
        }
        return event["css-classes"].map(escapeHtml).join(" ");
    };

    // set agenda date
    scheduler.templates.agenda_date = scheduler.templates.month_date;

    /* load the events */
    scheduler.attachEvent("onLoadError", function(xhr) {
        disableLoader();
        console.log("could not load events");
        console.log(xhr);
        showXHRError(xhr);
    });

    scheduler.attachEvent("onXLE", disableLoader);


    //requestJSON(schedulerUrl, loadEventsOnSuccess, loadEventsOnError);
    scheduler.setLoadMode("day");
    onCalendarInitialized();
    loadScheduler();
    //const dp = new dataProcessor(schedulerUrl);
    // use RESTful API on the backend
    //dp.setTransactionMode("REST");
    //dp.init(scheduler);

    setLoader();

    // set the actions we can use when clicking an event.
    // see https://docs.dhtmlx.com/scheduler/customizing_edit_select_bars.html
    scheduler.config.icons_select = [];
    getOwnProperties(actions).forEach(function(action) {
        let actionId = "icon_" + action;
        // Add this to the config.
        scheduler.config.icons_select.push(actionId);
        // Add an action.
        scheduler._click.buttons[action] = function(id){
            const event = scheduler.getEvent(id);
            actions[action](event);
         };
         /* Add a CSS style.
          * See https://codepen.io/noahblon/post/coloring-svgs-in-css-background-images
          * See https://css-tricks.com/change-color-of-svg-on-hover/ 
          * See https://stackoverflow.com/a/707580
          */
        const styleSheet = document.createElement("style");
        styleSheet.id = "icon-" + action;
        styleSheet.textContent = `.dhx_menu_icon.${actionId} {mask: url('/img/icons/${action}.svg');mask-size: 100%;}`;
        // Add a default text in case none is translated.
        document.head.appendChild(styleSheet);
        if (!OWCLocale.labels[actionId]) {
            OWCLocale.labels[actionId] = action;
            scheduler.i18n.setLocale(OWCLocale);
        }
    });
}

function loadScheduler() {
    scheduler.clearAll();
    let schedulerUrl = document.location.pathname.replace(/.html$/, ".events.json") + document.location.search;
    // add the time zone if not specified
    if (specification.timezone == "") {
        schedulerUrl += (document.location.search ? "&" : "?") + "timezone=" + getTimezone();
    }

    scheduler.load(schedulerUrl, "json");
    showLoader();
}

var onCalendarInitialized = onCalendarInitialized || function() {};

/* Agenda view
 *
 * see https://docs.dhtmlx.com/scheduler/agenda_view.html
 */

scheduler.date.agenda_start = function(date){
  return scheduler.date.month_start(new Date(date));
};

scheduler.date.add_agenda = function(date, inc){
  return scheduler.date.add(date, inc, "month");
};

/* Customize the week view
 *
 * See https://docs.dhtmlx.com/scheduler/custom_views.html
 */

scheduler.date.get_week_end=function(start_date){
  return scheduler.date.add(start_date, specification["start_of_week"] == "work" ? 5 : 7,"day");
}

/* Customize the month view so the work week is displayed.
 *
 * See
 */

scheduler.ignore_month = function(date){
  // 0 refers to Sunday, 6 - to Saturday
  if (date.getDay() == 6 || date.getDay() == 0) {
    return specification["start_of_week"] == "work";
    //hides Saturdays and Sundays
  }
};

scheduler.attachEvent("onBeforeViewChange", function(old_mode, old_date, mode, date){
    // see https://docs.dhtmlx.com/scheduler/api__scheduler_onbeforeviewchange_event.html
    // see https://forum.dhtmlx.com/t/scheduler-date-add-day-not-getting-called/35633
    // see https://docs.dhtmlx.com/scheduler/day_view.html#comment-6411743964
    if (mode == "day" && specification["start_of_week"] == "work") {
      if (date.getDay() == 6) {
        // Saturday, we come from Friday and go to Monday
        scheduler.setCurrentView(scheduler.date.add(date, 2, "day"));
        return false;
      } else if (date.getDay() == 0) {
        // Sunday, we come from Monday and go to Friday
        scheduler.setCurrentView(scheduler.date.add(date, -2, "day"));
        return false;
      }
    }
    return true;
});

async function getInformationAboutCalendars() {
    // see https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    const url = document.location.pathname.replace(/.html$/, ".json") + document.location.search;
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!response.ok) {
        showEventError(await response.json());
        throw new Error(`HTTP error! status: ${response.status}: ${response.text()}`);
    }
    return await response.json();
}

let calendarMetaData = null; // We only need to load this once.

async function loadCalendarMetadata() {
    // make the menu with the metadata work
    const toggleMenuButton = document.getElementById("menu__toggle");
    toggleMenuButton.addEventListener("change", function() {
        const otherCheckbox = document.getElementById("menu__toggle__2");
        if (otherCheckbox != null) {
            otherCheckbox.checked = toggleMenuButton.checked;
        }
    });
    // only update once
    if (calendarMetaData != null) {
        onCalendarInfoLoaded();
        return;
    }
    getInformationAboutCalendars().then( (info) => {
        calendarMetaData = info;
        onCalendarInfoLoaded();
    })
}

function onCalendarInfoLoaded() {
    // Since we had no data before, we set it now.
    console.log("Calendar Info:", calendarMetaData);
    const metaDataInMenu = document.getElementById("menu-meta-data");
    // fill the menu
    metaDataInMenu.appendChild(getMenuInnerContent(calendarMetaData));
    // handle errors
    for (error of calendarMetaData.errors) {
        showEventError(error);
    }
    // set the CSS variables
    // see https://stackoverflow.com/a/707794/1320237
    const sheet = document.createElement("style");
    sheet.id = "calendar-styles";
    for (const calendar of calendarMetaData.calendars) {
        const rules = "." + calendar["css-classes"][0] + ", ." +
            calendar["css-classes"][0] + " ." + calendar["css-classes"][1] + 
            " {" +
                (calendar.color ? " --dhx-scheduler-event-background: " +  calendar.color + "; " : "") +
                " --owc-menu-item-backgroud-color: var(--dhx-scheduler-event-background); " +
            "}";
        sheet.innerHTML += rules;
    }
    document.head.appendChild(sheet);
}

/* The menu is rendered each time we change the date.
 * The current state rests in this mapping.
 */

const calendarStatus = {};

function getCalendarMenuListElement(calendar) {
    /* For the content of the calendars
        * see open_web_calendar/convert/calendar.py
        */
    if (calendarStatus[calendar.id] == null) {
        /* Configure the style of how the calendar is displayed. */
        const status = calendarStatus[calendar.id] = {
            visible: true,
            calendar: calendar,
        };
        status.calendarStyleSheet = document.createElement("style");
        status.calendarStyleSheet.id = "calendar-menu-" + calendar.id;
        status.calendarStyleSheet.textContent = ""
        document.head.appendChild(status.calendarStyleSheet);
    }
    function toggleVisibility() {
        const status = calendarStatus[calendar.id];
        status.visible = !status.visible;
        console.log("display calendar change ", calendar.id, status.visible);
        status.calendarStyleSheet.textContent = `
            .event.${status.calendar["css-classes"][0]} {
                ${status.visible ? "" : "display: none;"}
            }`;
        console.log(status.calendarStyleSheet.textContent);
        calendarVisibilityToggle.checked = status.visible;
    }
    const status = calendarStatus[calendar.id];
    /* Add content to the calendar item. */
    const calendarListElement = document.createElement("div");
    const visibilityId = "calendar-visibility-" + calendar.id;
    calendarListElement.classList.add("menu__item");
    const calendarVisibilityToggle = document.createElement("input");
    if (specification.menu_shows_calendar_visibility_toggle) {
        // toggle visibility of a calendar
        calendarVisibilityToggle.type = "checkbox";
        calendarVisibilityToggle.classList.add("calendar-visibility-checkbox");
        calendarVisibilityToggle.checked = status.visible;
        calendarVisibilityToggle.onclick = toggleVisibility;
        calendarVisibilityToggle.id = visibilityId;
        calendarListElement.appendChild(calendarVisibilityToggle);
    }
    if (specification.menu_shows_calendar_names) {
        // calendar name
        const calendarName = document.createElement("label");
        calendarName.classList.add("calendar-title");
        calendarName.innerText = calendar.name;
        calendarVisibilityToggle.onclick = toggleVisibility;
        calendarName.htmlFor = visibilityId;
        calendarListElement.appendChild(calendarName)
    }
    if (specification.menu_shows_calendar_descriptions) {
        // calendar description
        const calendarDescription = document.createElement("div");
        calendarDescription.classList.add("calendar-description");
        calendarDescription.innerText = calendar.description;
        calendarListElement.appendChild(calendarDescription);
    }
    for (const cssClass of calendar["css-classes"]) {
        calendarListElement.classList.add(cssClass);
    }
    return calendarListElement;
}

function getMenuInnerContent(info) {
    // info is the metadata from /calendar.json
    const calendarInfoList = document.createElement("div");
    calendarInfoList.classList.add("calendar-list");
    for (const calendar of info.calendars) {
        calendarInfoList.appendChild(getCalendarMenuListElement(calendar));
    }
    return calendarInfoList;
}

window.addEventListener("load", loadCalendar);
window.addEventListener("load", loadCalendarMetadata);
