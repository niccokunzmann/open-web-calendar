"""Clean HTML content of events.

This is important to mitigate attacks from ICS sources.
See https://stackoverflow.com/questions/3073881/clean-up-html-in-python
"""


def clean_html(html:str, spec:dict) -> str:
    """Clean up the HTML.

    For the content of the spec parameter, see
    - the default_specification.yml file, clean_html_* attributes
    - https://lxml.de/api/lxml.html.clean.Cleaner-class.html
    """
    
