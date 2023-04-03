import translate
import pytest


@pytest.mark.parametrize(
    "language,file,id,expected_value",
    [
        ("en", "index", "language", "English"), 
        ("en", "_test", "id1", "test"), 
        ("en", "_test", "id2", "test2"), 
        ("de", "_test", "id1", "Test"), 
        ("de", "_test", "id2", "test2"), 
    ]
)
def test_translate(language, file, id, expected_value):
    """Translate the id."""
    assert translate.string(language, file, id) == expected_value



@pytest.mark.parametrize(
    "language,id,value",
    [
        ("en", "id2", '<span id="translate-id2" class="translation">test2</span>'), 
        ("en", "check-escape", '<span id="translate-check-escape" class="translation">&lt;nanana&gt;</span>'), 
    ]
)
def test_convert_html(language, id, value):
    """Check that html conversion works."""
    assert translate.html(language, "_test", id) == value
