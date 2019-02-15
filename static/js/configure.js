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

function loadCalendar() {
    // set format of dates in the data source
    //scheduler.config.xml_date="%Y-%m-%d %H:%i";
    // use UTC, see https://docs.dhtmlx.com/scheduler/api__scheduler_server_utc_config.html
    // scheduler.config.server_utc = true;
    scheduler.config.readonly = true;
    scheduler.init('scheduler_here', new Date(), "month");

    var urls = getQueries()["url"];
    if (urls) {
        scheduler.load(urls, "ical");
    } else {
        console.error("ERROR: no url parameter found, no calendar to display.");
    }
    
    //var dp = new dataProcessor(schedulerUrl);
    // use RESTful API on the backend
    //dp.setTransactionMode("REST");
    //dp.init(scheduler);
}

window.addEventListener("load", loadCalendar);

