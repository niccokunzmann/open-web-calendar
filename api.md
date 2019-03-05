# API

## Specification of the calendar

All parameters must be described sufficiently on the front page to use them.
If you add a new parameter,

- Add it to this file.
- Add it, if it with a default value to the [default_specification.json] file.
- Add an implementation, depending on its use in the app.py or the templates
  of the JavaScript files.
  The specification is already available in all of them, so you do not need to
  code that.

### Specification resolution

You can specify the calendar behavior and looks by these means.

1. **Query parameters**  
   All parameters to the calendar url are put into the specification.
   The query parameters have the highest precedence.
2. **specification_url**  
   If you specify this query parameter, the editor configuration is loaded from
   this url, too.
   Query parameters are still more important than what is written
   in this file.
   The source format can be YAML or JSON.
3. **[default_specification.json]**  
   This file contains the default parameters.
   They must not be hardcoded in the source code. They are there.
   Query parameters and the specification_url override these values.

### Parameter description

- `specification_url`  
  is a url to a specification file in case you do not want to pass parameters
  not as query strings but as a JSON file.
  For an example, see the [default_specification.json] file.

### Specification in the Calendar

[app.py](https://github.com/niccokunzmann/open-web-calendar/blob/85a72dab4561e250aec69b5ad7c3de074eefa1e8/app.py#L81) compiles the specification from the given parameters in `get_specification()`.
In the [template](https://github.com/niccokunzmann/open-web-calendar/blob/85a72dab4561e250aec69b5ad7c3de074eefa1e8/templates/calendars/dhtmlx.html#L23) you can access the specification through the `specification` variable.
The specification is available to JavaScript as the `specification` variable.

### Specification in the index page

The default specification is available before the calendar is built via JavaScript in the
`configuration.default_specification` variable.
There is a [getSpecification()](https://github.com/niccokunzmann/open-web-calendar/blob/85a72dab4561e250aec69b5ad7c3de074eefa1e8/static/js/index.js#L93) function which created the
specification from the inputs.

[default_specification.json]: ./default_specification.json
