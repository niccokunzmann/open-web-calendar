# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Check that we can customize the specification in various ways."""

import json
import os

import pytest

from open_web_calendar.app import DEFAULT_SPECIFICATION, get_default_specification

kv = pytest.mark.parametrize(("k", "v"), [("title", "test"), ("c", "d")])


@kv
def test_get_value_from_default_specification_dict(monkeypatch, k, v):
    """Check the the default spec value is considered."""
    monkeypatch.setitem(DEFAULT_SPECIFICATION, k, v)
    assert get_default_specification()[k] == v


def test_values_from_specification_file():
    """Check the values from the file are in here."""
    assert get_default_specification()["title"] == "Open Web Calendar"


def test_values_from_specification_file_are_overwritten_by_spec_dict(monkeypatch):
    """Check the values from the file are in here."""
    monkeypatch.setitem(DEFAULT_SPECIFICATION, "title", "other title")
    assert get_default_specification()["title"] == "other title"


@kv
def test_we_can_load_the_spec_from_a_file(tmp_path_factory, monkeypatch, k, v):
    """Check that the specification is enhanced by the temporary file.

    We also check that the order of specs is considered.
    """
    spec_path = tmp_path_factory.mktemp("spec") / "spec.json"
    spec_path.write_text(json.dumps({k: v}))
    monkeypatch.setitem(os.environ, "OWC_SPECIFICATION", str(spec_path))
    assert get_default_specification()[k] == v, "The values is loaded from a file."
    monkeypatch.setitem(os.environ, "OWC_SPECIFICATION", json.dumps({k: v + v}))
    assert get_default_specification()[k] == v + v, "The valus is loaded from JSON."
    monkeypatch.setitem(os.environ, "OWC_SPECIFICATION", f"{k}: '{v}{v}{v}'")
    assert get_default_specification()[k] == v + v + v, "The valus is loaded from YAML."
    monkeypatch.setitem(DEFAULT_SPECIFICATION, k, "other value")
    assert (
        get_default_specification()[k] == "other value"
    ), "The value in the app dict are more important."


def test_invalid_path_for_env_var(monkeypatch):
    """We can provide invalid values."""
    spec_path = "invalid-path/spec.json"
    monkeypatch.setitem(os.environ, "OWC_SPECIFICATION", str(spec_path))
    with pytest.raises(ValueError):
        get_default_specification()


# def test_invalid_value_for_env_var(tmp_path, monkeypatch):
#     """We can provide invalid values."""
#     monkeypatch.setitem(os.environ, "OWC_SPECIFICATION", "'invalid-config'")
#     with pytest.raises(ValueError):
#         get_default_specification()


def test_an_empty_spec_is_alright(monkeypatch):
    """The spec variable must be ok to be empty."""
    monkeypatch.setitem(os.environ, "OWC_SPECIFICATION", "")
    get_default_specification()


def test_no_spec_is_alright(monkeypatch):
    """Not having a spec is ok."""
    assert "OWC_SPECIFICATION" not in os.environ
    get_default_specification()
