"""Translations of the program into other languages."""
import os
import yaml
from html import escape
from markupsafe import Markup

HERE = os.path.dirname(__file__) or "."
TRANSLATIONS_PATH = os.path.join(HERE, "translations")

DEFAULT_LANGUAGE = "en"
DEFAULT_FILE = "common"
TRANSLATIONS = {}

# Parse the directory structure.
# translations/<lang>/<file>.yml
for language in os.listdir(TRANSLATIONS_PATH):
    TRANSLATIONS[language] = file_translations = {}
    language_path = os.path.join(TRANSLATIONS_PATH, language)
    for file in os.listdir(language_path):
        name, ext = os.path.splitext(file)
        with open(os.path.join(language_path, file)) as f:
            file_translations[name] =  yaml.safe_load(f)

def string(language: str, file: str, id: str) -> str:
    """Translate a string identified by language, file and id."""
    for source in (
        TRANSLATIONS.get(language, {}).get(file, {}),
        TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(file, {}),
        TRANSLATIONS.get(language, {}).get(DEFAULT_FILE, {}),
        TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(DEFAULT_FILE, {}),
    ):
        if id in source:
            return source[id]
    raise KeyError(f"The translation id '{id}' was not to be found in any file.")

def html(language: str, file: str, id: str) -> str:
    """Translate the string identified
    by language, file and id and return an html element.
    
    Any id ending in -html will not be escaped but treated as raw HTML.
    """
    inner_text = string(language, file, id)
    if not id.endswith("-html"):
        inner_text = escape(inner_text)
    id = escape(id)
    return Markup(f'<span id="translate-{id}" class="translation">{inner_text}</span>')


__all__ = ["html", "string"]
