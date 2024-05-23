# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Translations of the program into other languages."""
import os
import yaml
from html import escape
from markupsafe import Markup
from collections import defaultdict

HERE = os.path.dirname(__file__) or "."
TRANSLATIONS_PATH = os.path.join(HERE, "translations")

DEFAULT_LANGUAGE = "en"
DEFAULT_FILE = "common"
CALENDAR_FILE = "calendar"
TRANSLATIONS = {} # lang -> file -> id -> string
LANGUAGE_ALIAS = { # name also usable -> name in the translations directory
    "nb": "nb_NO",
    "ua": "uk",
    "jp": "ja",
    "cn": "zh_Hans",
    "no": "nb_NO",
} # rename language codes
UNUSED = "-unused"

# Parse the directory structure.
# translations/<lang>/<file>.yml
for language in os.listdir(TRANSLATIONS_PATH):
    TRANSLATIONS[language] = file_translations = defaultdict(dict)
    language_path = os.path.join(TRANSLATIONS_PATH, language)
    for file in os.listdir(language_path):
        name, ext = os.path.splitext(file)
        if ext != ".yml":
            continue
        if name.endswith(UNUSED):
            name = name[:-len(UNUSED)]
        with open(os.path.join(language_path, file)) as f:
            file_translations[name].update(yaml.safe_load(f))

def string(language: str, file: str, id: str) -> str:
    """Translate a string identified by language, file and id."""
    if "." in id:
        file, id = id.split(".", 1)
    language = LANGUAGE_ALIAS.get(language, language)
    for source in (
        TRANSLATIONS.get(language, {}).get(file, {}),
        TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(file, {}),
        TRANSLATIONS.get(language, {}).get(DEFAULT_FILE, {}),
        TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(DEFAULT_FILE, {}),
    ):
        if id in source:
            return source[id]
    raise KeyError(f"The translation id '{id}' was not to be found in any file.")

def html(language: str, file: str, id: str, **template_replacements) -> str:
    """Translate the string identified
    by language, file and id and return an html element.

    Any id ending in -html will not be escaped but treated as raw HTML.
    """
    inner_text = string(language, file, id)
    if template_replacements:
        inner_text = inner_text.format(**template_replacements)
    if not id.endswith("-html"):
        inner_text = escape(inner_text)
    id = escape(id)
    return Markup(f'<span id="translate-{id}" class="translation">{inner_text}</span>')


CALENDAR_LABELS = ["dhx_cal_today_button", "day_tab", "week_tab", "month_tab", "new_event", "icon_save", "icon_cancel", "icon_details", "icon_edit", "icon_delete", "confirm_closing", "confirm_deleting", "section_description", "section_time", "full_day", "confirm_recurring", "section_recurring", "button_recurring", "button_recurring_open", "button_edit_series", "button_edit_occurrence", "agenda_tab", "date", "description", "year_tab", "week_agenda_tab", "grid_tab", "drag_to_create", "drag_to_move", "message_ok", "message_cancel", "next", "prev", "year", "month", "day", "hour", "minute", "repeat_radio_day", "repeat_radio_week", "repeat_radio_month", "repeat_radio_year", "repeat_radio_day_type", "repeat_text_day_count", "repeat_radio_day_type2", "repeat_week", "repeat_text_week_count", "repeat_radio_month_type", "repeat_radio_month_start", "repeat_text_month_day", "repeat_text_month_count", "repeat_text_month_count2_before", "repeat_text_month_count2_after", "repeat_year_label", "select_year_day2", "repeat_text_year_day", "select_year_month", "repeat_radio_end", "repeat_text_occurences_count", "repeat_radio_end2", "repeat_radio_end3"]

def dhtmlx(language: str):
    """Create a dhtmlx scheduler custom locale from our translations.

    See also https://docs.dhtmlx.com/scheduler/localization.html
    """
    def cal(id):
        """Shortcut to get an id for the calendar."""
        return string(language, CALENDAR_FILE, id)
    result = {
        "labels": {
            "month_for_recurring": [
                cal("labels_month_for_recurring_jan"),
                cal("labels_month_for_recurring_feb"),
                cal("labels_month_for_recurring_mar"),
                cal("labels_month_for_recurring_apr"),
                cal("labels_month_for_recurring_may"),
                cal("labels_month_for_recurring_jun"),
                cal("labels_month_for_recurring_jul"),
                cal("labels_month_for_recurring_aug"),
                cal("labels_month_for_recurring_sep"),
                cal("labels_month_for_recurring_oct"),
                cal("labels_month_for_recurring_nov"),
                cal("labels_month_for_recurring_dec"),
            ],
            "day_for_recurring": [
                cal("labels_day_for_recurring_sun"),
                cal("labels_day_for_recurring_mon"),
                cal("labels_day_for_recurring_tue"),
                cal("labels_day_for_recurring_wed"),
                cal("labels_day_for_recurring_thu"),
                cal("labels_day_for_recurring_fri"),
                cal("labels_day_for_recurring_sat"),
            ]
        },
        "date": {
            "month_full": [
                cal("date_month_full_jan"),
                cal("date_month_full_feb"),
                cal("date_month_full_mar"),
                cal("date_month_full_apr"),
                cal("date_month_full_may"),
                cal("date_month_full_jun"),
                cal("date_month_full_jul"),
                cal("date_month_full_aug"),
                cal("date_month_full_sep"),
                cal("date_month_full_oct"),
                cal("date_month_full_nov"),
                cal("date_month_full_dec"),
            ],
            "month_short": [
                cal("date_month_short_jan"),
                cal("date_month_short_feb"),
                cal("date_month_short_mar"),
                cal("date_month_short_apr"),
                cal("date_month_short_may"),
                cal("date_month_short_jun"),
                cal("date_month_short_jul"),
                cal("date_month_short_aug"),
                cal("date_month_short_sep"),
                cal("date_month_short_oct"),
                cal("date_month_short_nov"),
                cal("date_month_short_dec"),
            ],
            "day_full": [
                cal("date_day_full_sun"),
                cal("date_day_full_mon"),
                cal("date_day_full_tue"),
                cal("date_day_full_wed"),
                cal("date_day_full_thu"),
                cal("date_day_full_fri"),
                cal("date_day_full_sat"),
            ],
            "day_short": [
                cal("date_day_short_sun"),
                cal("date_day_short_mon"),
                cal("date_day_short_tue"),
                cal("date_day_short_wed"),
                cal("date_day_short_thu"),
                cal("date_day_short_fri"),
                cal("date_day_short_sat"),
            ]
        }
    }
    for label in CALENDAR_LABELS:
        result["labels"][label] = cal("labels_" + label)
    return result


def dhtmlx_languages() -> list:
    """Return tuples of language name and language code."""
    result = set()
    for id in ("language", "language-en"):
        default = string(DEFAULT_LANGUAGE, "calendar", id)
        for code in TRANSLATIONS:
            language = string(code, "calendar", id)
            if language != default or code == DEFAULT_LANGUAGE:
                result.add((language, code))
    result = list(result)
    result.sort()
    return result


FILES = tuple(TRANSLATIONS[DEFAULT_LANGUAGE])

def strings_translated(language, files=FILES) -> int:
    """Return the number of translations strings."""
    language = LANGUAGE_ALIAS.get(language, language)
    return sum(len(TRANSLATIONS[language].get(file, {})) for file in files)


def fraction_translated(language, files=FILES) -> float:
    """Return the 0 <= fraction <= 1 of translation."""
    return 1.0*strings_translated(language, files) / strings_translated(DEFAULT_LANGUAGE, files)


def languages_for_the_index_file(minimal_fraction_translated=0.5):
    """Return a list of tuples of language name and code for all languages that are translated enough to offer the to a user.
    (language name, code, translated%)
    """
    files = ("index", "common")
    result = []
    for language, code in dhtmlx_languages():
        fraction = fraction_translated(code, files=files)
        if fraction >= minimal_fraction_translated:
            for other in result[:]:
                 if other[1] == code:
                     # merge languages with duplicate code
                     language = language + "/" + other[0]
                     result.remove(other)
            result.append([language, code, int(fraction * 100)])
    return result

__all__ = ["html", "string", "dhtmlx", "dhtmlx_languages", "fraction_translated", "strings_translated", "languages_for_the_index_file"]


if __name__ == "__main__":
    for language in sorted(TRANSLATIONS):
        print(f"{language} is {int(fraction_translated(language) * 100)}% translated: {strings_translated(language)}/{strings_translated(DEFAULT_LANGUAGE)}")
    print(f"These languages will be offered to the user: {', '.join(map(str, languages_for_the_index_file()))}")
