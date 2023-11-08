import requests

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.utils import get_admin_base_url
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.models import get_page_models
from wagtail.snippets.models import get_snippet_models


class Command(BaseCommand):
    """
    Checks the admin and frontend responses for models incl pages, snippets, settings and modeladmin.

    The command is only available in DEBUG mode. Set DEBUG=True in your settings to enable it.

    Basic usage:
        python manage.py report_responses <username> <password>

    Options:

        --host
            The URL to check. Defaults to the value of ADMIN_BASE_URL in settings.

        --report-url
            The URL to use for the report. e.g. http://staging.example.com

    Example:
        python manage.py report_responses <username> <password> \
            --report-url http://staging.example.com

        This will alter the displayed URLs in the report but the tested URL will still
        use the --host option.
    """

    help = "Checks the admin and frontend responses for models including pages, snippets, settings and modeladmin."

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            help="The username to use for login",
        )
        parser.add_argument(
            "password",
            help="The password to use for login",
        )
        parser.add_argument(
            "--host",
            default=get_admin_base_url(),
            help="The URL to check",
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

        if hasattr(settings, "DEVTOOLS_REGISTERED_MODELADMIN"):
            self.registered_modeladmin = settings.DEVTOOLS_REGISTERED_MODELADMIN
        else:
            self.registered_modeladmin = []

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
                # Login failed because the response isn't the Dashboard page
                self.out_message_error(
                    f"Could not log in to {options['host']}. Is the username and password correct?"
                )
                return

            # Reports models
            self.report_admin_home(session, options)
            self.report_page(session, options)
            self.report_snippets(session, options)
            self.report_modeladmin(session, options)
            self.report_settings_models(session, options)
            self.report_documents(session, options)
            self.report_images(session, options)

            # Reports admin pages
            self.report_search_page(session, options)
            self.report_locked_pages(session, options)
            self.report_workflows(session, options)
            self.report_workflow_tasks(session, options)
            self.report_site_history(session, options)
            self.report_aging_pages(session, options)

    def report_admin_home(self, session, options):
        self.out_message("\nChecking the admin home page (Dashboard) ...", "HTTP_INFO")

        admin_home_resp = session.get(f"{options['host']}/admin/")

        if admin_home_resp.status_code == 200:
            message = "\nAdmin home page ↓"
            self.out_message(message)
            self.out_message(f"{options['host']}/admin/ ← 200", "SUCCESS")
        else:
            message = "\nAdmin home page ↓"
            self.out_message(message)
            self.out_message(
                f"{options['host']}/admin/ ← {admin_home_resp.status_code}",
                "ERROR",
            )

    def report_page(self, session, options):
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

        # Print the index
        message = f"\nChecking the admin and frontend responses of {len(results)} page types ..."
        self.out_message(message, "HTTP_INFO")

        for count, content_type in enumerate(sorted(model_index)):
            message = (
                f" {count + 1}. {content_type}"
                if count <= 8  # Fixup the index number alignment
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

    def report_settings_models(self, session, options):
        self.out_message("\nChecking all SETTINGS edit pages ...", "HTTP_INFO")
        self.out_models(session, options, settings_registry)

    def report_documents(self, session, options):
        self.out_message("\nChecking the DOCUMENTS edit page ...", "HTTP_INFO")

        document_model = get_document_model()
        self.out_models(session, options, [document_model])

    def report_images(self, session, options):
        self.out_message("\nChecking the IMAGES edit page ...", "HTTP_INFO")

        image_model = get_image_model()
        self.out_models(session, options, [image_model])

    def report_search_page(self, session, options):
        self.out_message("\nChecking the Admin SEARCH page ...", "HTTP_INFO")

        url = f"{options['host']}/admin/pages/search/"

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def report_locked_pages(self, session, options):
        self.out_message("\nChecking the LOCKED PAGES page ...", "HTTP_INFO")

        url = f"{options['host']}/admin/reports/locked/"

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def report_workflows(self, session, options):
        self.out_message("\nChecking the WORKFLOWS page ...", "HTTP_INFO")

        url = f"{options['host']}/admin/reports/workflow/"

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def report_workflow_tasks(self, session, options):
        self.out_message("\nChecking the WORKFLOW TASKS page ...", "HTTP_INFO")

        url = f"{options['host']}/admin/reports/workflow_tasks/"

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def report_site_history(self, session, options):
        self.out_message("\nChecking the SITE HISTORY page ...", "HTTP_INFO")

        url = f"{options['host']}/admin/reports/site-history/"

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def report_aging_pages(self, session, options):
        self.out_message("\nChecking the AGING PAGES page ...", "HTTP_INFO")

        url = f"{options['host']}/admin/reports/aging-pages/"

        response = session.get(url)

        if response.status_code == 200:
            self.out_message(f"{url} ← 200", "SUCCESS")
        else:
            self.out_message(f"{url} ← {response.status_code}", "ERROR")

    def out_models(self, session, options, models):
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
