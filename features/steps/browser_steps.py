# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

from behave import given, when, then
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.common.exceptions import TimeoutException
import re


def specification_to_query(spec):
    """Convert the specification to a query string for the url."""
    result = []
    for k, v in spec.items():
        if not isinstance(v, list):
            v = [v]
        for v in v:
            result.append(urlencode({k: v}))
    return "&".join(result)


def get_url(context, url):
    """Replace getting the URL to mitigate a TimeoutException in Chrome."""
    print(f"Visiting {re.sub('^http://localhost:[0-9]+/', 'http://localhost:5000/', url)}")
    for i in range(20):
        try:
            return context.browser.get(url)
        except TimeoutException:
            pass


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
    get_url(context, url)
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
    events = context.browser.find_elements(By.XPATH, "//div[contains(@class, 'event')]")
    chosen_events = [event for event in events if text in event.get_attribute("innerText")]
    assert len(chosen_events) == 1, f"There should only be one event with the text {text} but there are {len(chosen_events)}: {chosen_events}"
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


@then('we cannot find an XPATH "{xpath}"')
def step_impl(context, xpath):
    elements = context.browser.find_elements(By.XPATH, xpath)
    for element in elements:
        print(element)
    assert not elements


@then(u'we cannot see the text "{text}"')
def step_impl(context, text):
    assert text not in get_body_text(context), f"{repr(text)} is visible but should not be visible"


@then(u'we can see the text "{text}"')
def step_impl(context, text):
    assert text in get_body_text(context), f"{repr(text)} is invisible but should be visible"


@then(u'we can see a {cls}')
def step_impl(context, cls):
    assert context.browser.find_elements(By.CLASS_NAME, cls), f"Expected to find elements of class {cls}"


@then('we can see an event with UID "{uid}" with css class "{css_class}"')
def step_impl(context, uid, css_class):
    """Make sure an event has a certain css class."""
    elements_by_uid = context.browser.find_elements(By.CLASS_NAME, f"UID-{uid}")
    elements_by_class = context.browser.find_elements(By.CLASS_NAME, css_class)
    found_elements = set(elements_by_uid) & set(elements_by_class)
    assert found_elements, f"Expected at least one event with UID {uid} to have the css class {css_class} but none did."


@then(u'we cannot see a {cls}')
def step_impl(context, cls):
    assert not context.browser.find_elements(By.CLASS_NAME, cls), f"Expected to not find elements of class {cls}"


@when(u"we open the about page")
def step_impl(context):
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


@when("we click on >")
def step_impl(context):
    """Move the calendar one section further."""
    click_button(context, By.CLASS_NAME, "dhx_cal_next_button")


@when("we click on <")
def step_impl(context):
    """Move the calendar one section further."""
    click_button(context, By.CLASS_NAME, "dhx_cal_prev_button")


def click_button(context, selector_type, selector):
    """Find a button with a selector and click it."""
    buttons = context.browser.find_elements(selector_type, selector)
    assert len(buttons) == 1, f"Expected one button but got {buttons}."
    buttons[0].click()


# Browser steps for configuring the calendar.


@given('we are on the configuration page')
def step_impl(context):
    """Visit the configuration page and wait for it to load."""
    context.browser.delete_all_cookies()
    url = context.index_page + "?" + specification_to_query(context.specification)
    get_url(context, url)


@when('we write "{text}" into "{field_id}"')
def step_impl(context, text, field_id):
    """Write text into text input."""
    input = context.browser.find_element(By.ID, field_id)
    input.clear() # see https://stackoverflow.com/a/7809907/1320237
    input.send_keys(text)
    print(f"Expecting {field_id}.value == {input.get_attribute('value')}")


@then('"{text}" is written in "{field_id}"')
def step_impl(context, text, field_id):
    """Check that a field has a value."""
    input = context.browser.find_element(By.ID, field_id)
    actual_text = input.get_attribute('value')
    assert actual_text == text, f"Expected {repr(text)} in {field_id} but got {repr(actual_text)}."


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
    try:
        return json.loads(json_string)
    except:
        print(repr(json_string))
        raise


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


@when(u'we click on the {tag:S} "{text}"')
def step_impl(context, tag, text):
    # select if inner text element equals the text
    # see https://stackoverflow.com/a/3655588/1320237
    elements = context.browser.find_elements(By.XPATH, f"//{tag}[text()[. = {repr(text)}]]")
    assert len(elements) == 1, f"There should only be one {tag} with the text {repr(text)} but there are {len(elements)}."
    element = elements[0]
    element.click()


@then('the checkbox with id "{id:S}" is checked')
def step_impl(context, id):
    """Check the checkbox status."""
    element = context.browser.find_element(By.ID, id)
    assert element.get_attribute("checked")


@then('the checkbox with id "{id}" is not checked')
def step_impl(context, id):
    """Check the checkbox status."""
    element = context.browser.find_element(By.ID, id)
    assert not element.get_attribute("checked")


@when('we click on the {tag_name:S} with id "{id}"')
def step_impl(context, tag_name, id):
    """Click on elements with an id."""
    element = context.browser.find_element(By.ID, id)
    element.click()


## Link verification

@then('the link "{link_text}" targets "{link_target}"')
def step_impl(context, link_text, link_target):
    """Check the target of a link."""
    assert_tag_with_text_attribute_equals(context, "a", link_text, "target", link_target)


@then('the link "{link_text}" opens "{link_href}"')
def step_impl(context, link_text, link_href):
    """Check the href of a link."""
    assert_tag_with_text_attribute_equals(context, "a", link_text, "href", link_href)


def assert_tag_with_text_attribute_equals(context, tag, text, attribute, expected_value):
    """Make sure that an attribute of a tag has a certain value."""
    # select if inner text element equals the text
    # see https://stackoverflow.com/a/3655588/1320237
    elements = context.browser.find_elements(By.XPATH, f"//{tag}[text()[contains(., {repr(text)})]]")
    assert len(elements) >= 1, f"Expected at least one <{tag}> with text {repr(text)} but got {len(elements)}."
    actual_values = [element.get_attribute(attribute) for element in elements]
    assert expected_value in actual_values, f"Expected a <{tag}> with the text {repr(text)} to have an attribute {attribute} with the value \n{repr(expected_value)} but the values are \n{{}}.".format('\n'.join(map(repr, actual_values)))

## Other
