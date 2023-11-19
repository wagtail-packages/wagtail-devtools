# Content Types Report

The `content_types` report will generate a report for all content types in the project.

Reports can be generated for:

- Pages
- Snippets
- Settings
- ModelAdmin

## Usage

Create a command class in your app's `management/commands` directory that inherits from `BaseContentTypes` with the following content:

```python
from wagtail_devtools.management.commands._base_content_types import (
    BaseContentTypesCommand,
)


class Command(BaseContentTypesCommand):
    apps_prefix = None  # or the root app name
    registered_modeladmin = [
        # Add your modeladmin classes here
        # e.g. "test.TestModelAdminModel",
    ]
    excluded_apps = [
        # Add any apps you want to exclude here
        # e.g. "wagtail_devtools",
    ]

    def run_command(
        self,
        content_type_pages,
        content_type_snippets,
        content_type_modeladmin,
        content_type_settings,
        all_content_types,
        options,
    ):
        # Only include the content types here that you are interested in.
        self.out_table(content_type_pages, "Page")
        self.out_table(content_type_snippets, "Snippet")
        self.out_table(content_type_modeladmin, "ModelAdmin")
        self.out_table(content_type_settings, "Settings")

        if index := self.validate_index(options, all_content_types):
            # Generates the list of edit links for the selected content type
            self.out_edit_links(options, all_content_types[index])
```

You can use any name for the command file, but it must be in a `management/commands` directory.

I'll use `report_content_types.py` as an example.

**Note:** The above example is a full report that uses all available checks.

Run the command with:

```bash
./manage.py report_content_types
```

Then enter the index number of the content type you want to generate edit links for.

Optionally you can add the `--cid` option to the command to skip the index selection prompt.
