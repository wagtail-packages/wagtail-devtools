import json

from io import StringIO

from django.core.management import call_command
from django.test import RequestFactory, TestCase

from wagtail_devtools.api.views import api_view


# from unittest.mock import patch


def mock_session_login():
    request = RequestFactory().get("/")
    request.session = {
        "wagtail_devtools": {
            "username": "admin",
            "password": "password",
            "sessionid": "1234567890",
        }
    }


class TestApiViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().get("/")
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)

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
