from wagtail_devtools.management.commands._base_content_types import (
    BaseContentTypesCommand,
)


class Command(BaseContentTypesCommand):
    apps_prefix = None
    registered_modeladmin = ["test.TestModelAdminOne"]
    excluded_apps = []

    def run_command(
        self,
        content_type_pages,
        content_type_snippets,
        content_type_modeladmin,
        content_type_settings,
        all_content_types,
        options,
    ):
        # Generates the initial list of content types
        self.out_table(content_type_pages, "Page")
        self.out_table(content_type_snippets, "Snippet")
        self.out_table(content_type_modeladmin, "ModelAdmin")
        self.out_table(content_type_settings, "Settings")

        # Validates the user input
        index = self.validate_index(all_content_types)

        # Generates the list of edit links for the selected content type
        self.out_edit_links(options, all_content_types[index])
