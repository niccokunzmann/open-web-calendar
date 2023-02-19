from behave import given, when, then
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def specification_to_query(spec):
    """Convert the specification to a query string for the url."""
    result = []
    for k, v in spec.items():
        if not isinstance(v, list):
            v = [v]
        for v in v:
            result.append(urlencode({k: v}))
    return "&".join(result)


@given('we add the calendar "{calendar_name}"')
def step_impl(context, calendar_name):
    assert not ".ics" in calendar_name
    calendar_url = context.calendars_url + calendar_name + ".ics"
    context.specification["url"].append(calendar_url)


@when(u'we look at {date}')
def step_impl(context, date):
    context.specification["date"] = date
    context.browser.delete_all_cookies()
    url = context.index_page + "calendar.html?" + specification_to_query(context.specification)
    context.browser.get(url)
    print(f"Visiting {url}")
    # wait until the loader has stopped spinning
    # see https://stackoverflow.com/a/53242626/1320237
    # see https://stackoverflow.com/a/26567563/1320237
    WebDriverWait(context.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id = "loader" and contains(@class, "hidden")]')))


@then(u'we see 1 event')
@then(u'we see {count} events')
def step_impl(context, count=1):
    events = context.browser.find_elements(By.XPATH, "//div[contains(@class, 'event')]")
    assert len(events) == count, f"Expected {count} events but {len(events)} were found: {repr(events)}"

@then(u'we see that event "{uid}" has the text "{text}"')
def step_impl(context, uid, text):
    events = context.browser.find_elements(By.XPATH, f"//div[contains(@event_id, {repr(uid)})]")
    assert len(events) == 1, f"There should only be one event with UID {uid} but there are {len(events)}."
    event = events[0]
    innerText = event.get_attribute("innerText")
    assert innerText == text, f"Expected {repr(text)} but got {repr(innerText)}"


@when(u'we click on the event "{text}"')
def step_impl(context, text):
    print(repr(f"//div[contains(@class, 'event') and contains(text(), '{text}')]"))
    events = context.browser.find_elements(By.XPATH, "//div[contains(@class, 'event')]")
    chosen_events = [event for event in events if text in event.get_attribute("innerText")]
    assert len(chosen_events) == 1, f"There should only be one event with the text {text} but there are {len(events)}."
    event = chosen_events[0]
    event.click()


def get_body_text(context):
    body = context.browser.find_elements(By.XPATH, "//body")[0]
    innerText = body.get_attribute("innerText")
    return innerText


@then(u'we cannot see the text "{text}"')
def step_impl(context, text):
    assert text not in get_body_text(context)


@then(u'we can see the text "{text}"')
def step_impl(context, text):
    assert text in get_body_text(context)


