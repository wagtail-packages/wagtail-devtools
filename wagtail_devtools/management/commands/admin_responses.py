import requests

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.utils import get_admin_base_url
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.models import get_page_models
from wagtail.models.collections import Collection
from wagtail.snippets.models import get_snippet_models


class Command(BaseCommand):
    """
    The command is only available in DEBUG mode. Set DEBUG=True in your settings to enable it.

    Basic usage:
        python manage.py admin_responses <username> <password>

    Options:
        --host
            The URL to check. Defaults to the value of ADMIN_BASE_URL in settings.
        --report-url
            The URL to use for the report. e.g. http://staging.example.com

    When using the --report-url option the displayed URLs in the report will be altered.
    This tested url will still use --host option.

    E.G. python manage.py admin_responses <username> <password> --report-url http://staging.example.com
    """

    help = "Checks the admin and frontend responses for models including pages, snippets, settings and modeladmin and more."

    def add_arguments(self, parser):
        parser.add_argument("username", help="The username to use for login")
        parser.add_argument("password", help="The password to use for login")
        parser.add_argument(
            "--host", default=get_admin_base_url(), help="The URL to check"
        )
        parser.add_argument(
            "--report-url",
            help="The URL to use for the report. e.g. http://staging.example.com",
        )

    def handle(self, *args, **options):
        # Disabled if not running in DEBUG mode
        if not settings.DEBUG:
            raise CommandError(
                "This command is only available in DEBUG mode. Set DEBUG=True in your settings to enable it."
            )

        self.report_lines = []
        self.checked_url = options["host"]
        self.report_url = (
            options["report_url"].strip("/") if options["report_url"] else None
        )

        with requests.Session() as session:
            url = f"{options['host']}/admin/login/"

            try:
                session.get(url)
            except requests.exceptions.ConnectionError:
                self.out_message_error(
                    f"Could not connect to {options['host']}. Is the server running?"
                )
                return
            except requests.exceptions.InvalidSchema:
                self.out_message_error(
                    f"Could not connect to {options['host']}. Invalid schema"
                )
                return
            except requests.exceptions.MissingSchema:
                self.out_message_error(
                    f"Could not connect to {options['host']}. Missing schema"
                )
                return

            # Attempt to log in
            logged_in = session.post(
                url,
                data={
                    "username": options["username"],
                    "password": options["password"],
                    "csrfmiddlewaretoken": session.cookies["csrftoken"],
                    "next": "/admin/",
                },
            ).content

            if "Forgotten password?" in logged_in.decode("utf-8"):
                # Login failed because the response is the forgotten password page
                self.out_message_error(
                    f"Could not log in to {options['host']}. Is the username and password correct?"
                )
                return

            # Reports admin list pages
            self.report_admin_list_pages(
                session, "admin home page (Dashboard)", f"{options['host']}/admin/"
            )
            self.report_admin_list_pages(
                session, "SEARCH", f"{options['host']}/admin/pages/search/"
            )
            self.report_admin_list_pages(
                session, "LOCKED PAGES", f"{options['host']}/admin/reports/locked/"
            )
            self.report_admin_list_pages(
                session, "WORKFLOWS LIST", f"{options['host']}/admin/reports/workflow/"
            )
            self.report_admin_app_model(
                session,
                options,
                "WORKFLOWS EDIT",
                app_label="wagtailcore",
                model_name="Workflow",
            )
            self.report_admin_list_pages(
                session,
                "WORKFLOWS TASKS",
                f"{options['host']}/admin/reports/workflow_tasks/",
            )
            self.report_admin_app_model(
                session,
                options,
                "WORKFLOWS TASK EDIT",
                app_label="wagtailcore",
                model_name="Task",
            )
            self.report_admin_list_pages(
                session,
                "SITE HISTORY",
                f"{options['host']}/admin/reports/site-history/",
            )
            self.report_admin_list_pages(
                session, "AGING PAGES", f"{options['host']}/admin/reports/aging-pages/"
            )

            # Reports models
            self.report_admin_list_pages(
                session, "USERS", f"{options['host']}/admin/users/"
            )
            self.report_users(session, options)
            self.report_admin_list_pages(
                session, "GROUPS", f"{options['host']}/admin/groups/"
            )
            self.report_groups(session, options)
            self.report_admin_list_pages(
                session, "SITES", f"{options['host']}/admin/sites/"
            )
            self.report_sites(session, options)
            self.report_admin_list_pages(
                session, "COLLECTIONS", f"{options['host']}/admin/collections/"
            )
            self.report_collections(session, options)
            self.report_admin_list_pages(
                session, "REDIRECTS", f"{options['host']}/admin/redirects/"
            )
            self.report_admin_app_model(
                session,
                options,
                "REDIRECTS EDIT",
                app_label="wagtailredirects",
                model_name="Redirect",
            )
            self.report_documents(session, options)
            self.report_images(session, options)
            self.report_settings_models(session, options)
            self.report_snippets(session, options)
            self.report_modeladmin(session, options)
            self.report_page(session, options)

    def report_admin_list_pages(self, session, title, url):
        self.out_message(f"\nChecking the {title} page ...", "HTTP_INFO")

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def report_admin_app_model(self, session, options, title, app_label, model_name):
        self.out_message(f"\nChecking the {title} page ...", "HTTP_INFO")

        model = apps.get_model(app_label, model_name)
        self.out_models(session, options, [model])

    def report_users(self, session, options):
        self.out_message("\nChecking the USERS EDIT page ...", "HTTP_INFO")

        user_model = get_user_model()
        self.out_models(session, options, [user_model])

    def report_groups(self, session, options):
        self.out_message("\nChecking the GROUPS EDIT page ...", "HTTP_INFO")

        group_model = apps.get_model("auth", "Group")
        self.out_models(session, options, [group_model])

    def report_sites(self, session, options):
        self.out_message("\nChecking the SITES EDIT page ...", "HTTP_INFO")

        site_model = apps.get_model("wagtailcore", "Site")
        self.out_models(session, options, [site_model])

    def report_collections(self, session, options):
        self.out_message("\nChecking the COLLECTIONS EDIT page ...", "HTTP_INFO")

        self.out_model(session, options, Collection.objects.first().get_first_child())

    def report_documents(self, session, options):
        self.out_message("\nChecking the DOCUMENTS edit page ...", "HTTP_INFO")

        document_model = get_document_model()
        self.out_models(session, options, [document_model])

    def report_images(self, session, options):
        self.out_message("\nChecking the IMAGES edit page ...", "HTTP_INFO")

        image_model = get_image_model()
        self.out_models(session, options, [image_model])

    def report_settings_models(self, session, options):
        self.out_message("\nChecking all SETTINGS edit pages ...", "HTTP_INFO")
        self.out_models(session, options, settings_registry)

    def report_snippets(self, session, options):
        self.out_message("\nChecking all SNIPPETS models edit pages ...", "HTTP_INFO")

        snippet_models = get_snippet_models()
        self.out_models(session, options, snippet_models)

    def report_modeladmin(self, session, options):
        if hasattr(settings, "DEVTOOLS_REGISTERED_MODELADMIN"):
            registered_modeladmin = settings.DEVTOOLS_REGISTERED_MODELADMIN
        else:
            registered_modeladmin = []

        self.out_message("\nChecking all MODELADMIN edit pages ...", "HTTP_INFO")

        modeladmin_models = []
        for model in apps.get_models():
            app = model._meta.app_label
            name = model.__name__
            if f"{app}.{name}" in registered_modeladmin:
                modeladmin_models.append(apps.get_model(app, name))

        self.out_models(session, options, modeladmin_models)

    def report_page(self, session, options):
        """Check and report the admin and frontend responses for all page model types."""
        page_models = self.filter_page_models(get_page_models())

        model_index = []
        results = []

        for page_model in page_models:
            if item := page_model.objects.first():
                model_index.append(item.__class__.__name__)
                results.append(
                    {
                        "title": item.title,
                        "url": f"{options['host']}{item.url}",
                        "id": item.id,
                        "editor_url": f"{self.get_admin_edit_url(options, item)}",
                        "class_name": item.__class__.__name__,
                    }
                )

        message = f"\nChecking the admin and frontend responses of {len(results)} page types ..."
        self.out_message(message, "HTTP_INFO")

        for count, content_type in enumerate(sorted(model_index)):
            # Also add padding for the single digit numbers
            message = (
                f" {count + 1}. {content_type}"
                if count <= 8
                else f"{count + 1}. {content_type}"
            )
            self.out_message(message)

        # Print the results
        for page in results:
            message = f"\n{page['title']} ( {page['class_name']} ) ↓"
            self.out_message(message)

            # Check the admin response
            response = session.get(page["editor_url"])
            if response.status_code != 200:
                self.out_message(
                    f"{page['editor_url']} ← {response.status_code}", "ERROR"
                )
            else:
                self.out_message(f"{page['editor_url']} ← 200", "SUCCESS")

            # Check the frontend response
            response = session.get(page["url"])
            if response.status_code == 200:
                self.out_message(f"{page['url']} ← 200", "SUCCESS")
            else:
                if response.status_code == 404:
                    message = (
                        f"{page['url']} ← {response.status_code} probably a draft page"
                    )
                    self.out_message(message, "WARNING")
                else:
                    self.out_message(f"{page['url']} ← {response.status_code}", "ERROR")

    def out_models(self, session, options, models):
        """Create a report for the first object of each model.
        The models have a base_manager that is used to get the first object."""
        for model in models:
            obj = model.objects.first()
            if not obj:
                # settings model has no objects
                continue

            url = self.get_admin_edit_url(options, obj)

            message = f"\n{model._meta.verbose_name.capitalize()} ↓"
            self.out_message(message)

            response = session.get(url)

            if response.status_code == 200:
                self.out_message(f"{url} ← 200", "SUCCESS")
            else:
                self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def out_model(self, session, options, model):
        """Create a report for the first object of a model.
        The model does not have a base_manager so the object is passed in."""
        url = self.get_admin_edit_url(options, model)

        message = f"\n{model.name} ↓"
        self.out_message(message)

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def out_message(self, message, style=None):
        if self.report_url:
            message = message.replace(self.checked_url, self.report_url)
        if message not in self.report_lines:
            self.report_lines.append(message)
        if style and style == "HTTP_INFO":
            self.stdout.write(self.style.HTTP_INFO(message))
            self.stdout.write("=" * len(message))
        elif style and style == "ERROR":
            self.stderr.write(self.style.ERROR(message))
        elif style and style == "SUCCESS":
            self.stdout.write(self.style.SUCCESS(message))
        elif style and style == "WARNING":
            self.stdout.write(self.style.WARNING(message))
        else:
            self.stdout.write(message)

    @staticmethod
    def filter_page_models(page_models):
        """Filter out page models that are not creatable or are in the core apps."""

        filtered_page_models = []

        for page_model in page_models:
            if page_model._meta.app_label == "wagtailcore":
                # Skip the core apps
                continue
            if not page_model.is_creatable:
                # Skip pages that can't be created
                continue
            filtered_page_models.append(page_model)

        return filtered_page_models

    @staticmethod
    def get_admin_edit_url(options, obj):
        admin_url_finder = AdminURLFinder()
        return f"{options['host']}{admin_url_finder.get_edit_url(obj)}"
