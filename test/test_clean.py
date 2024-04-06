"""Test cleaning the HTML input."""
import pytest
from clean_html import clean_html


@pytest.mark.parametrize(
    "input,spec,expected_output",
    [
        ("<div>a</div>", {"clean_html_remove_tags":["div"]}, "a"),
    ]
)
def test_clean_html_from_spec(input, spec, expected_output):
    """Specify how to clean the HTML content."""
    output = clean_html(input, spec=spec)
    assert output == expected_output
