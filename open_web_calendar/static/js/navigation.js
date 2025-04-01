// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only
/* This is used by the configuration page for navigation. */

function isSectionForConfig(section) {
    return !section.classList.contains("not-for-config");
}

function initializeNavigation() {
    const sectionsDropdown = document.getElementById("select-sections");
    const sections = document.getElementsByTagName("section");
    let lastSection = null;
    let uiIndexMax = 0;
    for (const section of sections) {
        if (isSectionForConfig(section)) {
            uiIndexMax += 1;
        }
    }
    let uiIndex = 0;
    for (const section of sections) {
        if (isSectionForConfig(section)) {
            uiIndex += 1;
        }
        const heading = section.getElementsByTagName("h2")[0];
        // link
        const link = document.createElement("a");
        link.href = "#" + section.id;
        link.innerText = section.owcHeading = heading.innerText;
        // add to dropdown to chooose
        const option = document.createElement("option");
        option.value = section.id;
        option.innerText = isSectionForConfig(section) ? `${uiIndex}/${uiIndexMax} - ${section.owcHeading}` : section.owcHeading;
        sectionsDropdown.appendChild(option);
        // linking sections to each other
        if (lastSection) {
            lastSection.owcNextSection = section;
        }
        section.owcPreviousSection = lastSection;
        section.owcNextSection = null;
        lastSection = section;
    }
    // setTimeout(scrollToCurrentSection, 0);
    scrollToCurrentSection();
    initializeSliders();
}

function initializeSliders() {
    const heightSlider = document.getElementById("height-slider");
    heightSlider.onmousedown = heightSlider.ontouchstart = startHeightAdjustment;
    const widthSlider = document.getElementById("width-slider");
    widthSlider.onmousedown = widthSlider.ontouchstart = startWidthAdjustment;
    function end() {
        document.body.classList.remove("sliding");
        updateOutputs();
    }
    overlay.onmousemove = function(event) {
        if (!slidingCallback) return;
        slidingCallback({x:event.pageX, y:event.pageY});
    }
    overlay.onmouseup = overlay.onmouseleave = function(event) {
        if (!slidingCallback) return;
        slidingCallback({x:event.pageX, y:event.pageY});
        end();
    };
    window.ontouchmove = function(event) {
        if (!slidingCallback) return;
        const touch = {x:event.changedTouches[0].pageX, y:event.changedTouches[0].pageY};
        slidingCallback(touch);
        event.preventDefault();
    }
    window.ontouchend = window.ontouchcancel = function(event) {
        if (!slidingCallback) return;
        const touch = {x:event.changedTouches[0].pageX, y:event.changedTouches[0].pageY};
        slidingCallback(touch);
        end();
    };
};

function scrollToCurrentSection() {
    let sectionId = document.location.hash;
    if (sectionId.startsWith("#")) {
        sectionId = sectionId.slice(1);
    }
    let sections = document.getElementsByTagName("section");
    let currentSection = sectionId ? document.getElementById(sectionId) : sections[0];
    if (currentSection == null) {
        currentSection = sections[0];
    }
    for (const section of sections) {
        section.classList.remove("active");
    }
    currentSection.classList.add("active");
    window.scrollTo({
        top: 0,
        left: window.innerWidth/2,
        behavior: "smooth",
      });
    const currentSectionLink = document.getElementById("currect-section");
    // currentSectionLink.href = "#" + currentSection.id;
    currentSectionLink.innerText = currentSection.owcHeading;
    // Set navigation for next and previous section
    const bottomNextLink = document.getElementById("bottom-next-link");
    const nextSectionLink = document.getElementById("navigate-next");
    if (currentSection.owcNextSection) {
        nextSectionLink.href = bottomNextLink.href = "#" + currentSection.owcNextSection.id;
        nextSectionLink.innerText = currentSection.owcNextSection.owcHeading;
        document.body.classList.remove("no-next-section");
    } else {
        document.body.classList.add("no-next-section");
    }
    const bottomPreviousLink = document.getElementById("bottom-previous-link");
    const previousSectionLink = document.getElementById("navigate-previous");
    if (currentSection.owcPreviousSection) {
        previousSectionLink.href = bottomPreviousLink.href = "#" + currentSection.owcPreviousSection.id;
        previousSectionLink.innerText = currentSection.owcPreviousSection.owcHeading;
        document.body.classList.remove("no-previous-section");
    } else {
        document.body.classList.add("no-previous-section");
    }
    const sectionsDropdown = document.getElementById("select-sections");
    sectionsDropdown.value = currentSection.id;
};

window.addEventListener("load", initializeNavigation);
window.addEventListener("hashchange", scrollToCurrentSection);

function updateHeightOfSlider(event) {
    // see https://www.w3schools.com/css/css3_variables_javascript.asp
    const textHeight = 21;
    let height = getTotalDocumentHeight() - event.y + textHeight;
    const display = document.getElementById("calendar-height");
    const scheduler = document.getElementById("open-web-calendar");
    const maxHeight = getTotalDocumentHeight() - scheduler.offsetHeight - textHeight;
    height = Math.max(textHeight, Math.min(maxHeight, height));
    document.body.style.setProperty('--bottom-slider-height', height + "px");
    display.innerText = scheduler.offsetHeight + "px";
}

function getTotalDocumentHeight() {
    // see https://stackoverflow.com/a/1147768/1320237
    const body = document.body;
    const html = document.documentElement;
    return Math.max( body.scrollHeight, body.offsetHeight, 
                        html.clientHeight, html.scrollHeight, html.offsetHeight );
}

function updateWidthOfSlider(event) {
    document.body.style.setProperty('--main-width', event.x + "px");
}

function startHeightAdjustment(event) {
    startSliding(updateHeightOfSlider);
    event.preventDefault();
}

function startWidthAdjustment() {
    startSliding(updateWidthOfSlider)
}

let slidingCallback = null;

function startSliding(callback) {
    // see https://stackoverflow.com/a/50238821/1320237
    const overlay = document.getElementById("overlay");
    document.body.style.setProperty('--total-document-height', getTotalDocumentHeight() + "px");
    document.body.classList.add("sliding");
    slidingCallback = callback;
}

function selectSection() {
    const select = document.getElementById("select-sections");
    const sectionId = select.options[select.selectedIndex].value;
    document.location.hash = sectionId;
}