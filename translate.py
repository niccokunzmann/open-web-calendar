"""Translations of the program into other languages."""
import os
import yaml
from html import escape
from markupsafe import Markup

HERE = os.path.dirname(__file__) or "."
TRANSLATIONS_PATH = os.path.join(HERE, "translations")

DEFAULT_LANGUAGE = "en"
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
    return TRANSLATIONS[language][file].get(id, TRANSLATIONS[DEFAULT_LANGUAGE][file][id])


def html(language: str, file: str, id: str) -> str:
    """Translate the string identified by language, file and id and return an html element."""
    inner_text = escape(string(language, file, id))
    id = escape(id)
    return Markup(f'<span id="translate-{id}" class="translation">{inner_text}</span>')


__all__ = ["html", "string"]
