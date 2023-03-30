/*
 * Common functions.
 */


function getTimezone() {
    // see https://stackoverflow.com/a/37512371
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}