import json

from io import StringIO

from django.core.management import call_command
from django.test import RequestFactory, TestCase

from wagtail_devtools.api.helpers import get_admin_edit_url
from wagtail_devtools.api.views import (
    api_view,
    wagtail_core_apps,
    wagtail_core_listing_pages,
)
from wagtail_devtools.test.models import HomePage


class TestApiViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)

    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_api_view(self):
        response = api_view(self.request)
        data = json.loads(response.content)["api-views"]
        self.assertEqual(len(data), 2)
        self.assertEqual(
            data[0],
            "http://localhost:8000/wagtail-devtools-api/listing-types/",
        )
        self.assertEqual(
            data[1],
            "http://localhost:8000/wagtail-devtools-api/wagtail-core-apps/",
        )

    def test_wagtail_core_listing_pages(self):
        response = wagtail_core_listing_pages(self.request)
        data = json.loads(response.content)["results"]

        self.assertEqual(len(data), 23)
        self.assertEqual(data[0]["title"], "Search promotions")
        self.assertEqual(data[0]["app_name"], "wagtailsearchpromotions")
        self.assertEqual(data[0]["class_name"], None)
        self.assertEqual(
            data[0]["editor_url"],
            "http://localhost:8000/admin/searchpicks/",
        )
        self.assertEqual(data[0]["url"], None)

    def test_wagtail_core_apps(self):
        response = wagtail_core_apps(self.request)
        data = json.loads(response.content)["results"]

        self.assertEqual(len(data), 34)
        self.assertEqual(data[0]["title"], "Home Page")
        self.assertEqual(data[0]["app_name"], "wagtail_devtools_test")
        self.assertEqual(data[0]["class_name"], "HomePage")

        # editor_url is different in different versions of wagtail
        home_page_editor_url = get_admin_edit_url(
            self.request, HomePage.objects.get(slug="home")
        )
        self.assertEqual(
            data[0]["editor_url"],
            home_page_editor_url,
        )
        self.assertEqual(data[0]["url"], HomePage.objects.get(slug="home").url)

    def test_wagtail_core_apps_all(self):
        self.request.GET = {"all": True}
        response = wagtail_core_apps(self.request)
        data = json.loads(response.content)["results"]

        self.assertEqual(len(data), 73)
        self.assertEqual(data[0]["title"], "Home Page")
        self.assertEqual(data[0]["app_name"], "wagtail_devtools_test")
        self.assertEqual(data[0]["class_name"], "HomePage")

        # editor_url is different in different versions of wagtail
        home_page_editor_url = get_admin_edit_url(
            self.request, HomePage.objects.get(slug="home")
        )
        self.assertEqual(
            data[0]["editor_url"],
            home_page_editor_url,
        )
        self.assertEqual(data[0]["url"], HomePage.objects.get(slug="home").url)
