// SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
//
// SPDX-License-Identifier: GPL-2.0-only
/* This is used by the calendar for sign up. */

function openSignUp(event) {
    const signUpDiv = document.getElementById("email-signup");
    signUpDiv.classList.remove("hidden");
    const signUpButton = document.getElementById("sign-up-button");
    signUpButton.onclick = function () {
        signUp(event);
    }
}

function cancelSignUp() {
    const signUpDiv = document.getElementById("email-signup");
    signUpDiv.classList.add("hidden");
}

function signUp(event) {
    const name = document.getElementById("signup-name").value;
    const email = document.getElementById("signup-email").value;
    const urls = specification.url;
    const calendarUrl = typeof urls == "string" ? urls : urls[event["calendar-index"]];
    const ical = event.ical;
    showLoader();
    sendSignUp({
        calendar: calendarUrl,
        email: email,
        name: name,
        event: ical,
    }).then((response)=> {
        disableLoader();
        cancelSignUp();
        loadScheduler();
        scheduler.hideQuickInfo();
        
    }, (error) => {
        disableLoader();
        // showEventError(error);
        showErrorWindows();
    })

}

async function sendSignUp(json) {
    // see https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    const url = "/caldav/sign-up";
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(json),
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



document.addEventListener("load", openSignUp);
