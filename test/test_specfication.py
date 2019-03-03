"""
This test the algorithm written
in the api.md file.
"""
import pytest
import sys
from werkzeug.datastructures import MultiDict
print(sys.path)


from app import get_specification, get_default_specification, cache_url
def test_specification_equals_default_specification_by_default():
    assert get_specification(query=MultiDict({})) == get_default_specification()

def test_specification_overrides_attributes_from_default_specification():
    assert get_default_specification()["css"] == ""
    assert get_specification(query=MultiDict({"css": "test"}))["css"] == "test"

with_url = pytest.mark.parametrize("url", [
    "https://tets.io/aksdkkj.json",
    "https://alskdj.asd.de/asld/asdasd.yml",
])
@with_url
def test_specification_prefers_url_over_default(url):
    cache_url(url, '{"css": "123"}')
    assert get_specification(query=MultiDict({"specification_url":url}))["css"] == "123"

@with_url
def test_url_parameters_are_more_important_than_specification_url(url):
    cache_url(url, '{"test": "123"}')
    assert get_specification(query=MultiDict({"specification_url":url, "test": "test"}))["test"] == "test"

@with_url
def test_specification_can_be_loaded_from_yml_files(url):
    cache_url(url, 'test: "123"')
    assert get_specification(query=MultiDict({"specification_url":url}))["test"] == "123"
