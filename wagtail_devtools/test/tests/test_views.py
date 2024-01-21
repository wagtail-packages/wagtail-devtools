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
        self.assertEqual(len(data), 2)
        self.assertEqual(
            data[0],
            "http://localhost:8000/wagtail-devtools-api/listing-types/",
        )
        self.assertEqual(
            data[1],
            "http://localhost:8000/wagtail-devtools-api/wagtail-core-apps/",
        )
