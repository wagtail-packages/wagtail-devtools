import os

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.urls import reverse
from playwright.sync_api import sync_playwright
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import Collection
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.conf import get_listing_pages_config


User = get_user_model()


class PlaywrightContext:
    def __init__(self, live_server_url):
        self.live_server_url = live_server_url

    def __enter__(self, *args, **kwargs):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=300,
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

        username = "superuser"
        password = "superuser"

        self.page.goto(f"{self.live_server_url}/admin/login/")
        self.page.get_by_placeholder("Enter your username").fill(username)
        self.page.get_by_placeholder("Enter password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
        return self.page

    def __exit__(self, *args, **kwargs):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()


class Command(BaseCommand):
    help = "Test all the pages in wagtail admin"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url", type=str, help="The url to test", default="http://localhost:8000"
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Test all the pages in wagtail admin",
        )

    def handle(self, *args, **options):
        url = options["url"] or "http://localhost:8000"

        with PlaywrightContext(url) as listing_pages:
            listing_config = get_listing_pages_config()
            for app in listing_config:
                list_url = f"{url}{reverse(app['listing_name'])}"
                response = listing_pages.goto(list_url)
                if response.status == 200:
                    print(f"Page {list_url} is working")
                else:
                    print(f"Page {list_url} is not working {response.status}")

        configuration = {
            "title": "Wagtail core edit pages",
            "apps": [],
        }

        results = []

        for a in apps.get_app_configs():
            if hasattr(settings, "DEVTOOLS_APPS_EXCLUDE"):
                if a.name in settings.DEVTOOLS_APPS_EXCLUDE:
                    continue
            configuration["apps"].append(
                {
                    "app_name": a.label,
                    "models": [apps.get_model(a.label, m).__name__ for m in a.models],
                }
            )

        for app in configuration["apps"]:
            models = apps.get_app_config(app["app_name"]).get_models()
            if not options["all"]:
                for model in models:
                    item = model.objects.first()
                    if isinstance(item, Collection):
                        item = Collection.objects.first().get_first_child()
                    if AdminURLFinder().get_edit_url(item):
                        results.append(f"{url}{AdminURLFinder().get_edit_url(item)}")
            else:
                for model in models:
                    items = model.objects.all()
                    if isinstance(items.first(), Collection):
                        for item in items:
                            results.append(
                                f"{url}{AdminURLFinder().get_edit_url(item)}"
                            )
                    snippet_models = [model.__name__ for model in get_snippet_models()]
                    if model.__name__ in snippet_models:
                        for item in items:
                            results.append(
                                f"{url}{AdminURLFinder().get_edit_url(item)}"
                            )
                    else:
                        for item in items:
                            if AdminURLFinder().get_edit_url(item):
                                results.append(
                                    f"{url}{AdminURLFinder().get_edit_url(item)}"
                                )

        with PlaywrightContext(url) as page:
            for result in results:
                response = page.goto(result)
                if response.status == 200:
                    print(f"Page {result} is working")
                else:
                    print(f"Page {result} is not working {response.status}")
