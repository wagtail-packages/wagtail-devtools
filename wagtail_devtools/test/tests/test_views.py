import json

from io import StringIO

from django.core.management import call_command
from django.test import RequestFactory, TestCase

from wagtail_devtools.api.views import api_view


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
        self.assertEqual(len(data), 7)
        self.assertEqual(
            data[0],
            "http://localhost:8000/wagtail-devtools-api/edit-types/",
        )
        self.assertEqual(
            data[1],
            "http://localhost:8000/wagtail-devtools-api/form-types/",
        )
        self.assertEqual(
            data[2],
            "http://localhost:8000/wagtail-devtools-api/listing-types/",
        )
        self.assertEqual(
            data[3],
            "http://localhost:8000/wagtail-devtools-api/modeladmin-types/",
        )
        self.assertEqual(
            data[4],
            "http://localhost:8000/wagtail-devtools-api/page-types/",
        )
        self.assertEqual(
            data[5],
            "http://localhost:8000/wagtail-devtools-api/settings-types/",
        )
        self.assertEqual(
            data[6],
            "http://localhost:8000/wagtail-devtools-api/snippet-types/",
        )

    def test_form_types(self):
        response = self.client.get("/wagtail-devtools-api/form-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_model_admin_types(self):
        response = self.client.get("/wagtail-devtools-api/modeladmin-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_page_model_types(self):
        response = self.client.get("/wagtail-devtools-api/page-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_settings_types(self):
        response = self.client.get("/wagtail-devtools-api/settings-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_snippet_types(self):
        response = self.client.get("/wagtail-devtools-api/snippet-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_listing_types(self):
        response = self.client.get("/wagtail-devtools-api/listing-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)

    def test_edit_types(self):
        response = self.client.get("/wagtail-devtools-api/edit-types/")
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)
