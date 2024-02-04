import os

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.urls import reverse
from playwright.sync_api import sync_playwright
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.conf import get_listing_pages_config


User = get_user_model()


class PlaywrightContext:
    def __init__(self, live_server_url, slow_mo, browser=False, viewport=None):
        self.live_server_url = live_server_url
        self.slow_mo = slow_mo
        self.viewport = viewport
        self.headless = self.set_headless(browser)
        self.viewport = self.set_viewport(viewport)

    def set_viewport(self, viewport):
        if not viewport:
            return {"width": 1024, "height": 768}
        width, height = viewport.split("x")
        return {"width": int(width), "height": int(height)}

    def set_headless(self, browser):
        return not browser

    def __enter__(self, *args, **kwargs):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
        )
        self.context = self.browser.new_context(
            viewport=self.viewport if self.viewport else None,
        )
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
    help = "Runs playwright tests on the wagtail admin and frontend pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            type=str,
            help="The url to test (default=http://localhost:8000)",
            default="http://localhost:8000",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Test all the pages in wagtail admin and frontend (slow)",
        )
        parser.add_argument(
            "--slow",
            type=int,
            help="Slow down the test by the given amount of milliseconds",
            default=0,
        )
        parser.add_argument(
            "--browser",
            action="store_true",
            help="Show the browser window",
        )
        parser.add_argument(
            "--viewport",
            type=str,
            help="Set the viewport size (e.g. 1024x768)",
        )

    def handle(self, *args, **options):
        url = options["url"] or "http://localhost:8000"

        with PlaywrightContext(
            url, options["slow"], options["browser"], options["viewport"]
        ) as listing_pages:
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
            for model in models:
                is_collection = model.__name__ == "Collection"
                is_snippet = model.__name__ in [
                    model.__name__ for model in get_snippet_models()
                ]

                if is_collection:
                    items = (
                        # don't include the root collection
                        [model.objects.first().get_first_child()]
                        if not options["all"]
                        else model.objects.all().exclude(depth=1)
                    )

                if is_snippet:
                    items = (
                        [model.objects.first()]
                        if not options["all"]
                        else model.objects.all()
                    )

                if not is_collection and not is_snippet:
                    # must be some other model that doesn't need special handling
                    items = (
                        [model.objects.first()]
                        if not options["all"]
                        else model.objects.all()
                    )

                for item in items:
                    if AdminURLFinder().get_edit_url(item):
                        results.append(f"{url}{AdminURLFinder().get_edit_url(item)}")

        with PlaywrightContext(
            url, options["slow"], options["browser"], options["viewport"]
        ) as page:
            for result in results:
                response = page.goto(result)
                if response.status == 200:
                    print(f"Page {result} is working")
                else:
                    print(f"Page {result} is not working {response.status}")
