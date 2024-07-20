// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only

/* This is used by the dhtmlx scheduler.
 *
 */

function parseDate(yyyy_mm_dd) {
    // parse a date without timezone information
    // see https://stackoverflow.com/questions/17545708/parse-date-without-timezone-javascript
    var numbers = yyyy_mm_dd.match(/(\d+)-0?(\d+)-0?(\d+)/)
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
    var qs = document.location.search;
    var tokens, re = /[?&]?([^=]+)=([^&]*)/g;
    qs = qs.split("+").join(" ");

    var queries = {};
    while (tokens = re.exec(qs)) {
        var id = decodeURIComponent(tokens[1]);
        var content = decodeURIComponent(tokens[2]);
        if (Array.isArray(queries[id])) {
            queries[id].push(content);
        } if (queries[id]) {
            queries[id] = [queries[id], content];
        } else {
            queries[id] = content;
        }
    }
    return queries;
}

// TODO: allow choice through specification
var GOOGLE_URL = "https://maps.google.com/maps?q=";
var OSM_URL = "https://www.openstreetmap.org/search?query=";

/* Create a link around the HTML text.
 * Use this instead of creating links manually because it also sets the
 * target according to the specification.
 */
function makeLink(url, html) {
  return "<a target='" + specification.target + "' href='" + escapeHtml(url) + "'>" + html + "</a>";
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
var template = {
    "plain_summary": function(event) {
        return escapeHtml(event.text);
    },
    "formatted_summary": function(event) {
      var summary = template.plain_summary(event);
      if (event.url) {
        summary = makeLink(event.url, "🔗 " + summary);
      }
      return summary;
    },
    "details": function(event) {
        var details = document.createElement("div");
        details.classList.add("details");
        details.innerHTML = event.description;
        // set the target of all the links
        var links = details.getElementsByTagName("a");
        for (var i = 0; i < links.length; i++) {
          var link = links[i];
          link.target = specification.target;
        }
        return details.outerHTML;
    },
    "location": function(event) {
        if (!event.location && !event.geo) {
            return "";
        }
        var text = escapeHtml(event.location || "🗺");
        var geoUrl;
        if (event.geo) {
            geoUrl = "https://www.openstreetmap.org/?mlon=" + encodeURIComponent(event.geo.lon) + "&mlat=" + encodeURIComponent(event.geo.lat) + "&#map=15/" + encodeURIComponent(event.geo.lat) + "/" + encodeURIComponent(event.geo.lon);
        } else {
            geoUrl = OSM_URL + encodeURIComponent(event.location);
        }
        return makeLink(geoUrl, text);
    },
    "debug": function(event) {
        return "<pre class='debug' style='display:none'>" +
            escapeHtml(JSON.stringify(event, null, 2)) +
            "</pre>"
    },
    "categories": function (event) {
      if (event.categories.length) {
          return '<b>| ' + event.categories.map(escapeHtml).join(" | ") + ' |</b> ';
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
    }
}

/* The files use a Scheduler variable.
* scheduler.locale is used to load the locale.
* This creates the required interface.
*/
var setLocale = function(){};
var Scheduler = {plugin:function(setLocale_){
    // this is called by the locale_??.js files.
    setLocale = setLocale_;
}};

function showError(element) {
    var icon = document.getElementById("errorStatusIcon");
    icon.classList.add("onError");
    var errors = document.getElementById("errorWindow");
    element.classList.add("item");
    errors.appendChild(element);
}

function toggleErrorWindow() {
    var scheduler_tag = document.getElementById("scheduler_here");
    var errors = document.getElementById("errorWindow");
    scheduler_tag.classList.toggle("hidden");
    errors.classList.toggle("hidden");
}

function showXHRError(xhr) {
    var iframe = document.createElement("iframe");
    iframe.srcdoc = xhr.responseText;
    iframe.className = "errorFrame";
    showError(iframe);
}

function showEventError(error) {
    // show an error created by app.py -> error_to_dhtmlx
    var div = document.createElement("div");
    div.innerHTML = "<h1>" + error.text + "</h1>" +
        "<a href='" + error.url + "'>" + error.url + "</a>" +
        "<p>" + error.description + "</p>" +
        "<pre>" + error.traceback + "</pre>";
    showError(div);
}

function disableLoader() {
    var loader = document.getElementById("loader");
    loader.classList.add("hidden");
}

function setLoader() {
    if (specification.loader) {
        var loader = document.getElementById("loader");
        var url = specification.loader.replace(/'/g, "%27");
        loader.style.cssText += "background:url('" + url + "') center center no-repeat;"
    } else {
        disableLoader();
    }
}

function getHeader() {
    // elements that do not occur in the list will always be permitted
    var useHeaderElement = {
      "prev": specification.controls.includes("previous") ,
      "date": specification.controls.includes("date"),
      "next": specification.controls.includes("next"),
      "day": specification.tabs.includes("day"),
      "week": specification.tabs.includes("week"),
      "month": specification.tabs.includes("month"),
      "today": specification.controls.includes("today"),
      "agenda": specification.tabs.includes("agenda"),
    }
    function showSelected(headerElements) {
      return headerElements.filter(function(element){
        return useHeaderElement[element] != false; // null for absent
      });
    }
    // switch the header to a compact one
    // see https://docs.dhtmlx.com/scheduler/touch_support.html
    if (window.innerWidth < Number.parseInt(specification.compact_layout_width)) {
        return {
            rows: [
                {
                    cols: showSelected([
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


/* Disable/Enable features based on touch/mouse-over gestures
 * see https://stackoverflow.com/a/52855084/1320237
 */
var IS_TOUCH_SCREEN = window.matchMedia("(pointer: coarse)").matches;
var HAS_TOOLTIP = !IS_TOUCH_SCREEN;

function loadCalendar() {
    /* Format the time of the hour.
     * see https://docs.dhtmlx.com/scheduler/settings_format.html
     * see https://docs.dhtmlx.com/scheduler/api__scheduler_hour_date_config.html
     */
    scheduler.config.hour_date = specification["hour_format"];
    var format = scheduler.date.date_to_str(scheduler.config.hour_date);
    setLocale(scheduler);
    // load plugins, see https://docs.dhtmlx.com/scheduler/migration_from_older_version.html#5360
    scheduler.plugins({
        agenda_view: true,
        multisource: true,
        quick_info: true,
        recurring: false,
        tooltip: HAS_TOOLTIP,
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
    	var step = 60 / hour_division;
    	var html = "";
    	for (var i=0; i<hour_division; i++){
    	    html += "<div style='height:44px;line-height:44px;'>"+format(date)+"</div>"; // TODO: This should be in CSS.
    	    date = scheduler.date.add(date, step, "minute");
    	}
    	return html;
    }
    scheduler.config.first_hour = parseInt(specification["starting_hour"]);
    scheduler.config.last_hour = parseInt(specification["ending_hour"]);
    var date = specification["date"] ? parseDate(specification["date"]) : new Date();
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
    if (HAS_TOOLTIP) {
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
            template.debug(event);
    }
    // see https://docs.dhtmlx.com/scheduler/api__scheduler_quick_info_date_template.html
    scheduler.templates.quick_info_date = function(start, end, event){
        return joinHtmlLines([template.date(start, end), template.categories(event)]);
    }

    // general style
    scheduler.templates.event_class=function(start,end,event){
        if (event.type == "error") {
            showEventError(event);
        }
        return event["css-classes"].map(escapeHtml).join(" ");
    };

    // set agenda date
    scheduler.templates.agenda_date = scheduler.templates.month_date;

    schedulerUrl = document.location.pathname.replace(/.html$/, ".events.json") +
        document.location.search;
    // add the time zone if not specified
    if (specification.timezone == "") {
        schedulerUrl += (document.location.search ? "&" : "?") + "timezone=" + getTimezone();
    }

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
    scheduler.load(schedulerUrl, "json");


    //var dp = new dataProcessor(schedulerUrl);
    // use RESTful API on the backend
    //dp.setTransactionMode("REST");
    //dp.init(scheduler);

    setLoader();
}

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

window.addEventListener("load", loadCalendar);
