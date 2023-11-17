# Admin Responses

The `admin_responses` command will make a requests to the admin interface using get requests for a range of models. It will write a response result to the console.

Reports can be generated for:

- Admin Listing and Edit pages
- Frontend Pages

You can also add admin reports covering:

- Snippets
- Settings
- ModelAdmin
- Pages
- and more...

## Usage

Create a command class in your app's `management/commands` directory thats inherits from `BaseAdminResponsesCommand` with the following content:

```python
from wagtail_devtools.management.commands._base_admin_responses import (
    BaseAdminResponsesCommand,
)


class Command(BaseAdminResponsesCommand):
    def get_reports(self, *args, **options):
        session = self._log_in(options)

        register_reports = [
            # Add your reports here
        ]
```

You can use any name for the command file, but it must be in the `management/commands` directory.

I'll use `report_responses.py` as an example.

### Page model reports

Will generate a report for all admin edit pages for all page type models and corresponding frontend pages.

It does this by automatically finding all page models, then using a get request it will check the response status code for the admin edit page and the frontend page.

#### Setup

Add the following item to the `register_reports` list:

```python
{
    "function": self.report_pages,
    "args": [session, options],
}
```

- `function` is the function that will be called to generate the report.
- `args` is a list of arguments that will need to be passed to the function.
  - `session` is the session object that will be used to make the requests.
  - `options` is the commands options object that is passed to the command.

#### Example Console Output

![Page Model Report](./assets/pages-output.jpg)

If your terminal allows it the links should be clickable.

Any pages that return a response code other than 200 will be highlighted in red.
