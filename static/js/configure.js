/* This is used by the dhtmlx scheduler.
 *
 */

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

var template = {
    "summary": function(event) {
        return "<div class='summary'>" +
          (event.url ? makeLink(event.url, event.text) : event.text) +
          "</div>";
    },
    "details": function(event) {
        return "<div class='details'>" + event.description + "</div>";
    },
    "location": function(event) {
        if (!event.location && !event.geo) {
            return "";
        }
        var text = event.location || "🗺";
        var geoUrl;
        if (event.geo) {
            geoUrl = "https://www.openstreetmap.org/?mlon=" + event.geo.lon + "&mlat=" + event.geo.lat + "&#map=15/" + event.geo.lat + "/" + event.geo.lon;
        } else {
            geoUrl = OSM_URL + encodeURIComponent(event.location);
        }
        return makeLink(geoUrl, text);
    },
    "debug": function(event) {
        return "<pre class='debug' style='display:none'>" +
            JSON.stringify(event, null, 2) +
            "</pre>"
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
    });
    // set format of dates in the data source
    scheduler.config.xml_date="%Y-%m-%d %H:%i";

    // responsive lightbox, see https://docs.dhtmlx.com/scheduler/touch_support.html
    scheduler.config.responsive_lightbox = true;
    resetConfig();
    scheduler.attachEvent("onBeforeViewChange", resetConfig);
    scheduler.attachEvent("onSchedulerResize", resetConfig);

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
    var date = specification["date"] ? new Date(specification["date"]) : new Date();
    scheduler.init('scheduler_here', date, specification["tab"]);

    // event in the calendar
    scheduler.templates.event_bar_text = function(start, end, event){
        return event.text;
    }
    // tooltip
    // see https://docs.dhtmlx.com/scheduler/tooltips.html
    if (HAS_TOOLTIP) {
        scheduler.templates.tooltip_text = function(start, end, event) {
            return template.summary(event) + template.details(event) + template.location(event);
        };
        scheduler.tooltip.config.delta_x = 1;
        scheduler.tooltip.config.delta_y = 1;
    }
    // quick info
    scheduler.templates.quick_info_title = function(start, end, event){
        return template.summary(event);
    }
    scheduler.templates.quick_info_content = function(start, end, event){
        return template.details(event) +
            template.location(event) +
            template.debug(event);
    }

    scheduler.templates.event_header = function(start, end, event){
        if (event.categories){
            return (scheduler.templates.event_date(start)+" - "+
                scheduler.templates.event_date(end)+'<b> | '+
	        event.categories)+' |</b>'
        } else {
            return(scheduler.templates.event_date(start)+" - "+
            scheduler.templates.event_date(end))
        }
    };

    // general style
    scheduler.templates.event_class=function(start,end,event){
        if (event.type == "error") {
            showEventError(event);
        }
        return event.type;
    };

    // set agenda date
    scheduler.templates.agenda_date = scheduler.templates.month_date;

    schedulerUrl = document.location.pathname.replace(/.html$/, ".events.json") +
        document.location.search;
    // add the time zone if not specified
    if (specification.timezone == "") {
        schedulerUrl += "&timezone=" + getTimezone();
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
