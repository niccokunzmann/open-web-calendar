
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

template = {
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


function loadCalendar() {
    setLocale(scheduler);
    // set format of dates in the data source
    scheduler.config.xml_date="%Y-%m-%d %H:%i";
    // use UTC, see https://docs.dhtmlx.com/scheduler/api__scheduler_server_utc_config.html
    scheduler.config.server_utc = true;
    scheduler.config.readonly = true;
    scheduler.init('scheduler_here', new Date(), "month");

    // event in the calendar
    scheduler.templates.event_bar_text = function(start, end, event){
        return event.text;
    }
    // tool tip
    // see https://docs.dhtmlx.com/scheduler/tooltips.html
    scheduler.templates.tooltip_text = function(start, end, event) {
        return template.summary(event) + template.details(event) + template.location(event);
    };
    dhtmlXTooltip.config.delta_x = 0;
    dhtmlXTooltip.config.delta_y = 0;
    // quick info
    scheduler.templates.quick_info_title = function(start, end, event){
        return template.summary(event);
    }
    scheduler.templates.quick_info_content = function(start, end, event){
        return template.details(event) +
            template.location(event) +
            template.debug(event);
    }
    // general style
    scheduler.templates.event_class=function(start,end,event){
        return "event";
    };

    schedulerUrl = document.location.pathname.replace(/.html$/, ".events.json") +
        document.location.search;

    scheduler.load(schedulerUrl, "json");

    //var dp = new dataProcessor(schedulerUrl);
    // use RESTful API on the backend
    //dp.setTransactionMode("REST");
    //dp.init(scheduler);
}

window.addEventListener("load", loadCalendar);
