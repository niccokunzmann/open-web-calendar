from behave import given, when, then
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json


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


@given('we set the "{parameter_name}" parameter to {parameter_value}')
def step_impl(context, parameter_name, parameter_value):
    context.specification[parameter_name] = json.loads(parameter_value)


@when(u'we look at {date}')
def step_impl(context, date):
    context.specification["date"] = date
    context.browser.delete_all_cookies()
    url = context.index_page + "calendar.html?" + specification_to_query(context.specification)
    context.browser.get(url)
    print(f"Visiting {url}")
    wait_for_calendar_to_load(context)

def wait_for_calendar_to_load(context):
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


@when('we click on a link containing "{text}"')
def step_impl(context, text):
    event = context.browser.find_element(By.XPATH, f"//a[contains(text(), {repr(text)})]")
    event.click()


def get_body_text(context):
    body = context.browser.find_elements(By.XPATH, "//body")[0]
    innerText = body.get_attribute("innerText")
    return innerText


@then(u'we cannot see the text "{text}"')
def step_impl(context, text):
    assert text not in get_body_text(context), f"{repr(text)} is visible but should not be visible"


@then(u'we can see the text "{text}"')
def step_impl(context, text):
    assert text in get_body_text(context), f"{repr(text)} is invisible but should be visible"


@then(u'we can see a {cls}')
def step_impl(context, cls):
    assert context.browser.find_elements(By.CLASS_NAME, cls), f"Expected to find elements of class {cls}"


@then(u'we cannot see a {cls}')
def step_impl(context, cls):
    assert not context.browser.find_elements(By.CLASS_NAME, cls), f"Expected to not find elements of class {cls}"


@when(u"we open the about page")
def step_impl(context):
    print([x for x in dir(context.browser) if "find" in x ])
    button = context.browser.find_element(By.ID, "infoIcon")
    button.click()
    WebDriverWait(context.browser, 10).until(EC.presence_of_element_located((By.ID, "translate-license")))

@when(u'we select "{dropdown_text}"')
def step_impl(context, dropdown_text):
    options = context.browser.find_elements(By.XPATH, f"//option[contains(text(), {repr(dropdown_text)})]")
    assert options, f"Could not find option with text {repr(dropdown_text)}"
    if len(options) != 1:
        print(f"Expected one option but found many: {', '.join(repr(o.get_attribute('innerText')) for o in options)}")
    option = options[0]
    option.click() # see https://stackoverflow.com/a/7972225/1320237
    wait_for_calendar_to_load(context)


# Browser steps for configuring the calendar.


@given('we are on the configuration page')
def step_impl(context):
    """Visit the configuration page and wait for it to load."""
    context.browser.delete_all_cookies()
    url = context.index_page + "?" + specification_to_query(context.specification)
    context.browser.get(url)
    print(f"Visiting {url}")


@when('we write "{text}" into "{field_id}"')
def step_impl(context, text, field_id):
    """Write text into text input."""
    input = context.browser.find_element(By.ID, field_id)
    input.clear() # see https://stackoverflow.com/a/7809907/1320237
    input.send_keys(text)
    print(f"{field_id}.value == {input.get_attribute('value')}")


@when('we write the date {day}/{month}/{year} into "{field_id}"')
def step_impl(context, year, month, day, field_id):
    """Write text into text input."""
    input = context.browser.find_element(By.ID, field_id)
    input.clear() # see https://stackoverflow.com/a/7809907/1320237
    # construct the text, see https://stackoverflow.com/a/35855868/1320237
    text = context.browser.execute_script(f"return (new Date({year}, {month} - 1, {day})).toLocaleDateString()")
    print("text =", repr(text))
    # For filling inputs and date inputs
    # see https://stackoverflow.com/a/35127217/1320237
    # see https://stackoverflow.com/a/39532746/1320237
    ActionChains(context.browser).move_to_element(input).click().send_keys(text).perform()
    value = input.get_attribute('value')
    if not value:
        # this works in Chrome, see https://stackoverflow.com/a/21314269/1320237
        context.browser.execute_script(f'document.getElementById({repr(field_id)}).value = "{year}-{month}-{day}"');
        input.send_keys(Keys.CONTROL)
        value = input.get_attribute('value')
    print(f"{field_id}.value == {value}")


@when('we choose "{choice}" in "{select_id}"')
def step_impl(context, choice, select_id):
    """Write text into text input."""
    element = context.browser.find_element(By.ID, select_id)
    # see https://stackoverflow.com/a/28613320/1320237
    select = Select(element)
    select.select_by_visible_text(choice)
    print(f"{select_id} selected {repr(element.get_attribute('value'))} though text {repr(choice)}")


def get_specification(context) -> dict:
    """Return the specification from the configuration page."""
    spec_element = context.browser.find_element(By.ID, "json-specification")
    json_string = spec_element.get_attribute("innerText")
    return json.loads(json_string)


def assert_specification_has_value(context, attribute, expected_value="no value"):
    """Make sure the specification has a certain value."""
    specification = get_specification(context)
    actual_value = specification.get(attribute, "no value")
    assert actual_value == expected_value, f"specification.{attribute}: expected {expected_value} but got {actual_value}."


@then('"{attribute}" is specified as {expected_value}')
def step_impl(context, attribute, expected_value):
    """Check the JSON value of an attribute."""
    assert_specification_has_value(context, attribute, json.loads(expected_value))


@then('"{attribute}" is not specified')
def step_impl(context, attribute):
    """Check the JSON value of an attribute."""
    assert_specification_has_value(context, attribute)


@when(u'we click on the {tag} "{text}"')
def step_impl(context, tag, text):
    # select if inner text element equals the text
    # see https://stackoverflow.com/a/3655588/1320237
    elements = context.browser.find_elements(By.XPATH, f"//{tag}[text()[. = {repr(text)}]]")
    assert len(elements) == 1, f"There should only be one {tag} with the text {repr(text)} but there are {len(elements)}."
    element = elements[0]
    element.click()
