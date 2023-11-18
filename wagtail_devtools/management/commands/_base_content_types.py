from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.utils import get_admin_base_url
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.models import Page
from wagtail.snippets.models import get_snippet_models


class BaseContentTypesCommand(BaseCommand):
    """Base command for content types commands.

    This command is used to generate a report of all the admin edit pages for a given content type by entering the C-Type ID.

    The command is only available in DEBUG mode. Set DEBUG=True in your settings to enable it.

    The command will generate a list of all the content types in your project, and then prompt you to enter a C-Type ID from the list.

    The command will then generate a list of all the edit pages for that content type.

    To implement this command in your project, create a management command that extends this class.
    Add the following attributes to your command:

    apps_prefix = str() optional # The prefix of the apps you want to include in the report
    registered_modeladmin = [] # A list of modeladmin models you want to include in the report
    excluded_apps = [] # A list of apps you want to exclude from the report
    """

    help = "Generate a report of all the admin edit pages for a given content type by entering the C-Type ID."

    def add_arguments(self, parser):
        parser.add_argument(
            "--host",
            default=get_admin_base_url(),
            help="The URL to check",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.out_message_warning(
                "Command is only available in DEBUG mode. Set DEBUG=True in your settings to enable it."
            )
            return

        self.out_message_warning("\nUsing this command:")
        self.out_message("Enter a C-Type ID from the list below")
        self.out_message("to view a report of all the admin edit pages of that type.")

        content_types = ContentType.objects.filter(
            app_label__in=self.get_apps_for_pages_report(
                self.apps_prefix, self.excluded_apps
            )
        ).order_by("model", "app_label")

        if not content_types:
            self.out_message_warning("No content types found.")
            return

        content_type_pages = self.get_contenttype_for_pages(content_types)
        content_type_snippets = self.get_contenttype_for_snippets(content_types)
        content_type_modeladmin = self.get_contenttypes_for_modeladmin(content_types)
        content_type_settings = self.get_contenttypes_for_settings(content_types)

        all_content_types = {
            **content_type_pages,
            **content_type_snippets,
            **content_type_modeladmin,
            **content_type_settings,
        }

        if not all(all_content_types):
            self.out_message_error("No content types found.")
            return

        self.run_command(
            content_type_pages,
            content_type_snippets,
            content_type_modeladmin,
            content_type_settings,
            all_content_types,
            options,
        )

    def validate_index(self, all_content_types):
        index = input("\nC-Type ID: ")

        try:
            index = int(index)
        except ValueError:
            self.out_message_error("Value must be an integer.")
            exit()

        if index not in all_content_types:
            self.out_message_error(f"Invalid C-Type ID: {index}")
            exit()

        return index

    def get_contenttypes_for_settings(self, content_types):
        content_type_settings = {}
        settings_models = []
        for model in settings_registry:
            settings_models.append(
                f"{model._meta.app_label}.{model._meta.model_name}".lower()
            )

        for content_type in content_types:
            model_str = f"{content_type.app_label}.{content_type.model}"
            if model_str in settings_models:
                content_type_settings[content_type.id] = [
                    content_type.model_class().__name__,
                    content_type.app_label,
                ]

        return content_type_settings

    def get_contenttypes_for_modeladmin(self, content_types):
        content_type_modeladmin = {}
        modeladmin_models = [model.lower() for model in self.registered_modeladmin]

        for content_type in content_types:
            model_str = f"{content_type.app_label}.{content_type.model}"
            if model_str in modeladmin_models:
                content_type_modeladmin[content_type.id] = [
                    content_type.model_class().__name__,
                    content_type.app_label,
                ]

        return content_type_modeladmin

    def get_contenttype_for_snippets(self, content_types):
        content_type_snippets = {}
        snippet_models = [model.__name__.lower() for model in get_snippet_models()]

        for content_type in content_types:
            if content_type.model in snippet_models:
                content_type_snippets[content_type.id] = [
                    content_type.model_class().__name__,
                    content_type.app_label,
                ]

        return content_type_snippets

    def get_contenttype_for_pages(self, content_types):
        content_type_pages = {}

        for content_type in content_types:
            cls = apps.get_model(content_type.app_label, content_type.model)
            if issubclass(cls, Page):
                content_type_pages[content_type.id] = [
                    content_type.model_class().__name__,
                    content_type.app_label,
                ]

        return content_type_pages

    def out_table(self, data, model_type=None):
        self.out_message_info(f"\nIndex of {model_type} Types")

        headers = ["Model", "App", "C-Type ID"]
        max_col_width = self.calc_col_width(data)

        self.out_message("-" * max_col_width * len(headers))
        self.out_message(
            " ".join([f"{header: <{max_col_width}}" for header in headers])
        )
        self.out_message("-" * max_col_width * len(headers))

        for key, row in data.items():
            self.out_message(
                " ".join([f"{col: <{max_col_width}}" for col in row]) + f" {key}"
            )

        self.out_message("-" * max_col_width * len(headers))

    def calc_col_width(self, data):
        max_col_width = 0
        for row in data.values():
            for col in row:
                if len(col) > max_col_width:
                    max_col_width = len(col)

        max_col_width += 6  # add some right padding
        return max_col_width

    def out_edit_links(self, options, data):
        model = apps.get_model(data[1], data[0])
        objects = model.objects.all()

        self.out_message_success(f"\nEdit Links for {data[0]}")
        self.out_message("-" * 70)

        title_field = None

        if hasattr(model, "title"):
            title_field = "title"
        elif hasattr(model, "name"):
            title_field = "name"

        for obj in objects:
            if title_field:
                t = getattr(obj, title_field)
                title = t[:30] + "..." if len(t) > 30 else t
                self.out_message(f"{title}")
            self.out_message(f"{self.get_admin_edit_url(options, obj)}\n\n")

    def out_message_warning(self, message):
        self.stdout.write(self.style.WARNING(message))

    def out_message(self, message):
        self.stdout.write(message)

    def out_message_error(self, message):
        self.stdout.write(self.style.ERROR(message))

    def out_message_info(self, message):
        self.stdout.write(self.style.HTTP_INFO(message))

    def out_message_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    @staticmethod
    def get_admin_edit_url(options, obj):
        admin_url_finder = AdminURLFinder()
        return f"{options['host']}{admin_url_finder.get_edit_url(obj)}"

    @staticmethod
    def get_apps_for_pages_report(apps_prefix=None, excluded_apps=None):
        """Return a list of apps we care about for the page types report."""

        if not apps_prefix:
            apps = [
                app
                for app in settings.INSTALLED_APPS
                if not app.split(".")[0] in excluded_apps
            ]
            return apps

        return [
            app.split(".")[1]
            for app in settings.INSTALLED_APPS
            if app.startswith(apps_prefix)
        ]
