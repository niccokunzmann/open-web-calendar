# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

import contextlib
import difflib
import json
import re
import time
from typing import Callable
from urllib.parse import urlencode, urljoin

from behave import given, then, when
from selenium.common.exceptions import (
    InvalidSessionIdException,
    JavascriptException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import Select, WebDriverWait

# default wait time in seconds
WAIT = 10


def wait_until(condition: Callable[[], bool], error_message: str):
    """Wait until the condition is true.

    Raise a TimeoutError if the condition is not met.
    """
    end = time.time() + WAIT
    while time.time() < end:
        value = condition()
        if value:
            return value
        time.sleep(0.01)
    raise TimeoutError(error_message)


@contextlib.contextmanager
def no_time_to_wait_for_elements(context):
    """Set the global wait to 0 and expect everythign to be there."""
    context.browser.implicitly_wait(0)
    yield
    context.browser.implicitly_wait(WAIT)


def specification_to_query(spec):
    """Convert the specification to a query string for the url."""
    result = []
    for k, vs in spec.items():
        for v in vs if isinstance(vs, list) else [vs]:
            result.append(urlencode({k: v}))
    return "&".join(result)


def get_url(context, url):
    """Replace getting the URL to mitigate a TimeoutException in Chrome."""
    print(
        f"Visiting {re.sub('^http://localhost:[0-9]+/', 'http://localhost:5000/', url)}"
    )
    with contextlib.suppress(InvalidSessionIdException):
        context.browser.delete_all_cookies()
        context.browser.execute_script('SELENIUM_IS_LOADING_A_NEW_PAGE_NOW="set value"')
    context.browser.get(url)
    end = time.time() + WAIT
    while time.time() < end:
        try:
            while (
                context.browser.execute_script(
                    'return SELENIUM_IS_LOADING_A_NEW_PAGE_NOW=="set value"'
                )
                and time.time() < end
            ):
                time.sleep(0.01)
        except JavascriptException:
            pass
        # see https://stackoverflow.com/a/36590395/1320237
        while (
            context.browser.execute_script("return document.readyState") != "complete"
            and time.time() < end
        ):
            time.sleep(0.01)
        if context.browser.current_url == url:
            break
        # if time.time() > end:
        #     raise TimeoutException("timed out!")
        assert context.browser.current_url == url, (
            f"Expecting to visit {url} but I am stuck on {context.browser.current_url}"
        )
    # print("DEBUG: current url", context.browser.current_url)


@given('we add the calendar "{calendar_name}"')
def step_impl(context, calendar_name):
    """Add a calendar to the url field.

    If there is no ending, .ics is added.
    """
    if "." not in calendar_name:
        calendar_name += ".ics"
    calendar_url = urljoin(context.calendars_url, calendar_name)
    context.specification["url"].append(calendar_url)


@given('we set the "{parameter_name}" parameter to {parameter_value}')
def step_impl(context, parameter_name, parameter_value):
    context.specification[parameter_name] = json.loads(parameter_value)


@when("we look at {date}")
def step_impl(context, date):
    context.specification["date"] = date
    url = (
        context.index_page
        + "calendar.html?"
        + specification_to_query(context.specification)
    )
    get_url(context, url)
    wait_for_calendar_to_load(context)


@given("we open the url from issue 563")
def step_impl(context):
    url = (
        "calendar.html?language=zh_Hans&url=https%3A%2F%2Fwww.calendarlabs.com%2Fica"
        "l-calendar%2Fics%2F46%2FGermany_Holidays.ics&url=%22%3E%3Cimg%20src%3Dx%20o"
        "nerror%3Dscheduler_here.innerText=%27hacked%27%3E"
    )
    get_url(context, context.index_page + url)
    wait_for_calendar_to_load(context)


def wait_for_calendar_to_load(context):
    # wait until the loader has stopped spinning
    # see https://stackoverflow.com/a/53242626/1320237
    # see https://stackoverflow.com/a/26567563/1320237
    WebDriverWait(context.browser, WAIT).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@id = "loader" and contains(@class, "hidden")]')
        )
    )


@then("we see 1 event")
@then("we see {count} events")
def step_impl(context, count=1):
    WebDriverWait(context.browser, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'event')]"))
    )
    events = context.browser.find_elements(
        By.XPATH, "//div[contains(@class, ' event ')]"
    )
    assert len(events) == count, (
        f"Expected {count} events but {len(events)} were found: {events!r}"
    )


@then('we see that event "{uid}" has the text "{text}"')
def step_impl(context, uid, text):
    events = context.browser.find_elements(
        By.XPATH, f"//div[contains(@event_id, {uid!r})]"
    )
    assert len(events) == 1, (
        f"There should only be one event with UID {uid} but there are {len(events)}."
    )
    event = events[0]
    inner_text = re.sub(r"\s+", " ", event.get_attribute("innerText"))
    assert inner_text == text, f"Expected {text!r} but got {inner_text!r}"


def get_events_with_text(context, text: str) -> list:
    """Return events with the text."""
    events = context.browser.find_elements(
        By.XPATH, "//div[contains(@class, ' event ')]"
    )
    return [event for event in events if text in event.get_attribute("innerText")]


@then('we can see the event "{text}"')
def step_impl(context, text):
    chosen_events = get_events_with_text(context, text)
    assert len(chosen_events) >= 1, (
        f"There should be one event with the text {text} "
        f"but there are none: {chosen_events}"
    )


@when('we click on the event "{text}"')
def step_impl(context, text):
    chosen_events = get_events_with_text(context, text)
    assert len(chosen_events) == 1, (
        f"There should only be one event with the text {text} "
        f"but there are {len(chosen_events)}: {chosen_events}"
    )
    event = chosen_events[0]
    event.click()


@when('we click on a link containing "{text}"')
def step_impl(context, text):
    xpath = f"//a[contains(text(), {text!r})]"
    # from https://stackoverflow.com/a/27603477/1320237
    link = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    # see also https://stackoverflow.com/a/9678084/1320237
    link.send_keys(Keys.CONTROL)
    link.send_keys(Keys.RETURN)
    link.click()
    time.sleep(0.1)


@when('we click on the link "{text}"')
@when('we click the link "{text}"')
def step_impl(context, text):
    links = context.browser.find_elements(By.XPATH, f"//a[text() = {text!r}]")
    assert len(links) == 1, (
        f"I should click on the link {text!r} but found {len(links)}."
    )
    links[0].click()


@when('we click on the first link "{text}"')
@when('we click the first link "{text}"')
def step_impl(context, text):
    links = context.browser.find_elements(By.XPATH, f"//a[text() = {text!r}]")
    assert len(links) >= 1, f"I should click on the link {text!r} but found none."
    links[0].click()


def get_body_text(context):
    end = time.time() + WAIT
    while end > time.time():
        try:
            body = context.browser.find_elements(By.XPATH, "//body")[0]
            text = body.get_attribute("innerText")
        except StaleElementReferenceException:  # noqa: PERF203
            time.sleep(0.01)
        else:
            if text is None:
                continue
            return text
    raise AssertionError("Could not get body text")


@then('we cannot find an XPATH "{xpath}"')
def step_impl(context, xpath):
    with no_time_to_wait_for_elements(context):
        elements = context.browser.find_elements(By.XPATH, xpath)
    for element in elements:
        print(element)
    assert not elements


@then('we cannot see the text "{text}"')
def step_impl(context, text):
    body = get_body_text(context)
    index = body.find(text)
    start = 0 if index < 10 else index - 10
    end = -1 if index > len(body) else index + 10
    assert index == -1, (
        f"{text!r} is visible but should not be visible: {body[start:end]!r}"
    )


@then('we can see the text "{text}"')
def step_impl(context, text):
    end = time.time() + WAIT
    while time.time() < end:
        if text in get_body_text(context):
            return
        time.sleep(0.01)
    raise AssertionError(f"{text!r} is invisible but should be visible")


@then("we can see a {cls}")
def step_impl(context, cls):
    assert context.browser.find_elements(By.CLASS_NAME, cls), (
        f"Expected to find elements of class {cls}"
    )


@then('we can see an event with UID "{uid}" with css class "{css_class}"')
def step_impl(context, uid, css_class):
    """Make sure an event has a certain css class."""
    elements_by_uid = context.browser.find_elements(By.CLASS_NAME, f"UID-{uid}")
    elements_by_class = context.browser.find_elements(By.CLASS_NAME, css_class)
    found_elements = set(elements_by_uid) & set(elements_by_class)
    assert found_elements, (
        f"Expected at least one event with UID {uid} "
        f"to have the css class {css_class} but none did."
    )


@then("we cannot see a {cls}")
def step_impl(context, cls):
    with no_time_to_wait_for_elements(context):
        assert not context.browser.find_elements(By.CLASS_NAME, cls), (
            f"Expected to not find elements of class {cls}"
        )


@when("we open the about page")
def step_impl(context):
    button = context.browser.find_element(By.ID, "infoIcon")
    button.click()
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "translate-license"))
    )


@when('we select "{dropdown_text}"')
def step_impl(context, dropdown_text):
    options = context.browser.find_elements(
        By.XPATH, f"//option[contains(text(), {dropdown_text!r})]"
    )
    assert options, f"Could not find option with text {dropdown_text!r}"
    if len(options) != 1:
        print(
            f"Expected one option but found many: "
            f"{', '.join(repr(o.get_attribute('innerText')) for o in options)}"
        )
    option = options[0]
    option.click()  # see https://stackoverflow.com/a/7972225/1320237
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

CALLS = 0


@given("we configure the {_id}")
def step_impl(context, _id):
    """Visit the configuration page and wait for it to load."""
    global CALLS  # noqa: PLW0603
    CALLS += 1
    context.browser.execute_script("SELENIUM_IS_LOADING_A_NEW_PAGE_NOW=true")
    if _id == "urls":
        assert context.current_recording != "", (
            "If you want to configure urls, load an api recording first. "
            "Otherwise we might get timeouts."
        )
    context.browser.delete_all_cookies()
    spec = context.specification.copy()
    spec["__test_calls"] = CALLS
    url = context.index_page + "?" + specification_to_query(spec) + "#configure-" + _id
    # with contextlib.suppress(TimeoutException):
    #     # the reload seems to be needed
    #     get_url(context, context.index_page + "?reload=true")
    get_url(context, url)
    if _id != "is-not-possible":
        # see https://stackoverflow.com/a/59130336/1320237
        WebDriverWait(context.browser, WAIT).until(
            EC.visibility_of_element_located((By.ID, "configure-" + _id))
        )


@when('we write "{text}" into "{field_id}"')
def step_impl(context, text, field_id):
    """Write text into text input."""
    end = time.time() + WAIT
    while time.time() < end:
        with contextlib.suppress(StaleElementReferenceException):
            input_element = context.browser.find_element(By.ID, field_id)
            with contextlib.suppress(StaleElementReferenceException):
                input_element.clear()  # see https://stackoverflow.com/a/7809907/1320237
            try:
                ActionChains(context.browser).scroll_to_element(
                    input_element
                ).send_keys_to_element(input_element, text).send_keys_to_element(
                    input_element, Keys.SHIFT
                ).perform()
            except (WebDriverException, StaleElementReferenceException) as e:
                print("Error", e)
                input_element.clear()  # see https://stackoverflow.com/a/7809907/1320237
                input_element.send_keys(text)
                # input_element.key_up(Keys.SHIFT)
            print(
                f"Expecting {field_id}.value == {input_element.get_attribute('value')}"
            )
            return
        time.sleep(0.01)


@then('"{text}" is written in "{field_id}"')
@then('"" is written in "{field_id}"')
def step_impl(context, field_id, text=""):
    """Check that a field has a value."""
    input_element = context.browser.find_element(By.ID, field_id)
    end = time.time() + WAIT
    while time.time() < end:
        actual_text = input_element.get_attribute("value")
        if actual_text != "":
            break
        time.sleep(0.01)
    assert actual_text == text, (
        f"Expected {text!r} in {field_id} but got {actual_text!r}."
    )


@then('"{text}" is not written in "{field_id}"')
@then('"" is not written in "{field_id}"')
def step_impl(context, field_id, text=""):
    """Check that a field has not a value."""
    input_element = context.browser.find_element(By.ID, field_id)
    actual_text = input_element.get_attribute("value")
    assert actual_text != text, (
        f"Expected a different text than {text!r} in {field_id}."
    )


@when('we write the date {day}/{month}/{year} into "{field_id}"')
def step_impl(context, year, month, day, field_id):
    """Write text into text input."""
    input_element = context.browser.find_element(By.ID, field_id)
    input_element.clear()  # see https://stackoverflow.com/a/7809907/1320237
    # construct the text, see https://stackoverflow.com/a/35855868/1320237
    text = context.browser.execute_script(
        f"return (new Date({year}, {month} - 1, {day})).toLocaleDateString()"
    )
    print("text =", repr(text))
    # For filling inputs and date inputs
    # see https://stackoverflow.com/a/35127217/1320237
    # see https://stackoverflow.com/a/39532746/1320237
    ActionChains(context.browser).move_to_element(input_element).click().send_keys(
        text
    ).perform()
    value = input_element.get_attribute("value")
    if not value:
        # this works in Chrome, see https://stackoverflow.com/a/21314269/1320237
        context.browser.execute_script(
            f'document.getElementById({field_id!r}).value = "{year}-{month}-{day}"'
        )
        input_element.send_keys(Keys.CONTROL)
        value = input_element.get_attribute("value")
    print(f"{field_id}.value == {value}")


@when('we choose "{choice}" in "{select_id}"')
def step_impl(context, choice, select_id):
    """Write text into text input."""
    # see https://stackoverflow.com/a/28613320/1320237
    end = time.time() + WAIT
    selected = None
    selected_text = None
    while not selected and time.time() < end:
        with contextlib.suppress(StaleElementReferenceException):
            element = context.browser.find_element(By.ID, select_id)
            select = Select(element)
            for i, option in enumerate(select.options):
                text = option.text
                if choice in text:
                    select.select_by_index(i)
                    selected = option
                    selected_text = text
                    # break
        if not selected:
            time.sleep(0.01)
    try:
        element = context.browser.find_element(By.ID, select_id)
        select = Select(element)
        print(
            f"{select_id} selected {element.get_attribute('value')!r} "
            f"through text {choice!r}, showing "
            f"{select.first_selected_option.text!r} {selected_text!r}"
        )
    except Exception as e:  # noqa: BLE001
        print(e)
        print(f"Error: {select_id}: {selected_text}")


def get_specification(context) -> dict:
    """Return the specification from the configuration page."""
    return context.browser.execute_script("return getSpecification()")


def assert_specification_has_value(context, attribute, expected_value="no value"):
    """Make sure the specification has a certain value."""
    end = time.time() + WAIT
    while time.time() < end:
        specification = get_specification(context)
        actual_value = specification.get(attribute, "no value")
        if actual_value == expected_value:
            return
        time.sleep(0.01)
    raise AssertionError(
        f"specification.{attribute}: expected {expected_value} but got {actual_value}."
    )


@then('"{attribute}" is specified as {expected_value}')
def step_impl(context, attribute, expected_value):
    """Check the JSON value of an attribute."""
    try:
        expected = json.loads(expected_value)
    except json.JSONDecodeError as e:
        raise ValueError(f"The feature contains invalid JSON: {expected_value}") from e
    assert_specification_has_value(context, attribute, expected)


@then('"{attribute}" is not specified')
def step_impl(context, attribute):
    """Check the JSON value of an attribute."""
    assert_specification_has_value(context, attribute)


@when('we click the button "{text}"')
def click_the_button(context, text):
    """Click the only button with this label."""
    selector = (
        By.XPATH,
        f"//input[@type = 'button' and contains(@value, {text!r})]"
        " | "
        f"//button[contains(., {text!r})]",
    )
    print("selector", selector)
    WebDriverWait(context.browser, WAIT).until(
        EC.visibility_of_element_located(selector)
    )
    buttons = context.browser.find_elements(*selector)
    assert len(buttons) == 1, (
        f"Expected one button with the text {text!r} but got {buttons}."
    )
    # buttons[0].focus()
    buttons[0].send_keys(Keys.RETURN)


@when('we click on the {tag:S} "{text}"')
def step_impl(context, tag, text):
    if tag == "button":
        click_the_button(context, text)
        return
    # select if inner text element equals the text
    # see https://stackoverflow.com/a/3655588/1320237
    elements = context.browser.find_elements(By.XPATH, f"//{tag}[text()[. = {text!r}]]")
    if not elements:
        elements = context.browser.find_elements(
            By.XPATH, f"//{tag}[text()[contains(., {text!r})]]"
        )
    assert len(elements) == 1, (
        f"There should only be one {tag} with the text "
        f"{text!r} but there are {len(elements)}."
    )
    element = elements[0]
    element.click()


@when("we wait for the loader to disappear")
def step_impl(context):
    """Wait for the loader to disappaer."""
    wait_for_calendar_to_load(context)


@when('we click on the first {tag:S} "{text}"')
def step_impl(context, tag, text):
    # select if inner text element equals the text
    # see https://stackoverflow.com/a/3655588/1320237
    elements = context.browser.find_elements(By.XPATH, f"//{tag}[text()[. = {text!r}]]")
    if not elements:
        elements = context.browser.find_elements(
            By.XPATH, f"//{tag}[text()[contains(., {text!r})]]"
        )
    assert len(elements) >= 1, (
        f"There should have at least one {tag} with the text "
        f"{text!r} but there are {len(elements)}."
    )
    element = elements[0]
    element.click()
    # if tag == "button":
    #     element.send_keys(Keys.RETURN)


@then('the checkbox with id "{eid:S}" is checked')
def step_impl(context, eid):
    """Check the checkbox status."""
    end = time.time() + WAIT
    while time.time() < end:
        element = context.browser.find_element(By.ID, eid)
        if element.get_attribute("checked"):
            break
        time.sleep(0.01)
    assert element.get_attribute("checked")


@then('the checkbox with id "{eid}" is not checked')
def step_impl(context, eid):
    """Check the checkbox status."""
    element = context.browser.find_element(By.ID, eid)
    end = time.time() + WAIT
    while time.time() < end:
        if not element.get_attribute("checked"):
            break
        time.sleep(0.01)
    assert not element.get_attribute("checked")


@when('we click on the {tag_name:S} with id "{eid}"')
def step_impl(context, tag_name, eid):
    """Click on elements with an id."""
    element = context.browser.find_element(By.ID, eid)
    element.click()


## Link verification


@then('the link "{link_text}" targets "{link_target}"')
def step_impl(context, link_text, link_target):
    """Check the target of a link."""
    assert_tag_with_text_attribute_equals(
        context, "a", link_text, "target", link_target
    )


@then('the link "{link_text}" opens "{link_href}"')
@then('the link "{link_text}" opens ""')
def step_impl(context, link_text, link_href=""):
    """Check the href of a link."""
    assert_tag_with_text_attribute_equals(context, "a", link_text, "href", link_href)


@then('the link "{link_text}" opens nothing')
def step_impl(context, link_text):
    """Check the href of a link."""
    link_href = context.browser.current_url + "#"
    assert_tag_with_text_attribute_equals(context, "a", link_text, "href", link_href)


def assert_tag_with_text_attribute_equals(
    context, tag, text, attribute, expected_value
):
    """Make sure that an attribute of a tag has a certain value."""
    # select if inner text element equals the text
    # see https://stackoverflow.com/a/3655588/1320237
    elements = context.browser.find_elements(
        By.XPATH, f"//{tag}[text()[contains(., {text!r})]]"
    )
    assert len(elements) >= 1, (
        f"Expected at least one <{tag}> with text {text!r} but got {len(elements)}."
    )
    actual_values = [element.get_attribute(attribute) for element in elements]
    assert expected_value in actual_values, (
        f"Expected a <{tag}> with the text {text!r} to have an attribute "
        f"{attribute} with the value \n{expected_value!r} but the values are "
        f"\n{{}}.".format("\n".join(map(repr, actual_values)))
    )


## Other

CHECK = ".checked"


@then('we download the file "{file_name}"')
def step_impl(context, file_name: str):
    """Check that we downloaded the file."""
    print("Test download directory:     ", context.download_directory)
    print("Reference download directory:", context.expected_download_directory)
    file_check = context.download_directory / (file_name + CHECK)
    file_expected = context.expected_download_directory / file_name
    file_downloaded = context.download_directory / file_name
    previous_test = file_check.read_text() if file_check.exists() else ""
    assert not previous_test, (
        f"{file_name} was checked by {previous_test}. Choose another name!"
    )
    # get the step name
    # see https://stackoverflow.com/a/73913239
    file_check.write_text(f"{context.feature}-{context.step_name}")
    assert file_expected.exists(), f"The file we expect should exist!: {file_expected}"
    all_files = list(map(str, context.download_directory.iterdir()))
    for file in all_files[:]:
        if file.endswith(CHECK):
            all_files.remove(file)
            with contextlib.suppress(ValueError):
                all_files.remove(file[: -len(CHECK)])

    wait_until(
        lambda: file_downloaded.exists() and file_downloaded.read_text(),
        f'The file "{file_name}" should exist as "{file_downloaded}". '
        f"Instead we have {', '.join(all_files)}.",
    )
    l1 = file_downloaded.read_text().splitlines()
    l2 = file_expected.read_text().splitlines()
    for line in difflib.unified_diff(
        l1, l2, fromfile=str(file_downloaded), tofile=str(file_expected)
    ):
        print(line)
    assert l1 == l2, f"The file {file_name} is not the same as the expected file."


@given("we enable encryption")
def step_impl(context):
    """Enable encryption.

    This is disabled after each scenario.
    """
    context.server.enable_encryption()
    context.after_scenario.append(context.server.disable_encryption)


@then("we can see the password")
def step_impl(context):
    """The password is a text input."""
    element = context.browser.find_element(By.ID, "encryption-password")
    assert element.get_attribute("type") == "text"


@then("we cannot see the password")
def step_impl(context):
    """The password is a password input."""
    element = context.browser.find_element(By.ID, "encryption-password")
    assert element.get_attribute("type") == "password"


@when("we reload the page")
def refresh(context):
    """Reload the page."""
    # see https://stackoverflow.com/a/52546865/1320237
    context.browser.refresh()
    WebDriverWait(context.browser, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//body"))
    )


@given('we load the api recording "{recording}"')
def step_impl(context, recording: str):
    """Load a recording."""
    context.server.start_recorded_api(recording)
    context.after_scenario.append(context.server.stop_recorded_api)
    context.current_recording = recording


@when("we click on the menu")
def step_impl(context):
    """Click on the burger menu to open or close it."""
    element = context.browser.find_element(By.ID, "burger-menu-label")
    element.click()


def normalize_css_value(s):
    """Normalize the color and other values."""
    # rgb(231, 128, 116)
    color_match = re.match(r"rgb\((\d+),\s*(\d+),\s+(\d+)\)", s)
    if color_match:
        return "#" + "".join(
            hex(int(c))[2:].ljust(2, "0") for c in color_match.groups()
        )
    return s


@then('"{text}" has the {css_property} "{css_value}"')
def step_impl(context, text, css_property, css_value):
    """Check the background color of an item."""
    elements = context.browser.find_elements(
        By.XPATH, f"//*[contains(text(), {text!r})]"
    )
    assert elements, f"Cannot find any element with the text {text!r}"
    default_skip_to_parent = ["rgba(0, 0, 0, 0)"]
    for i, element in enumerate(elements):
        # see https://stackoverflow.com/a/15117720/1320237
        for _ in range(10):
            # search until body
            # see https://dev.to/pavel_polivka/determining-the-effective-background-color-17ld
            element_css_value = element.value_of_css_property(css_property)
            if element_css_value not in default_skip_to_parent:
                break
            print("skip to parent")
            try:
                new_element = element.find_element(By.XPATH, "..")
            except JavascriptException as e:
                # Message: Cyclic object value: [object HTMLDocument]
                raise AssertionError(
                    "Could not find any value for the element or the element is absent."
                ) from e
            assert new_element != element
            element = new_element  # noqa: PLW2901
        element_css_value = normalize_css_value(element_css_value)
        assert element_css_value == css_value, (
            f"Element {i}/{len(elements)} should have css "
            f"{css_property} set to {css_value!r} but the "
            f"value is {element_css_value!r}"
        )
