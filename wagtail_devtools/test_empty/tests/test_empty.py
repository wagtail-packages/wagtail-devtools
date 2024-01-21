from django.test import TestCase, override_settings

from wagtail_devtools.api.serializers import (
    form_types_serializer,
    model_admin_types_serializer,
    page_model_types_serializer,
    settings_types_serializer,
    snippet_types_serializer,
    wagtail_core_edit_pages_serializer,
    wagtail_core_listing_pages_serializer,
)
from wagtail_devtools.test_empty.settings import INSTALLED_APPS


class TestSerializers(TestCase):
    def test_form_types_serializer(self):
        ret = form_types_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 1)
        self.assertEqual(ret["results"][0]["title"], "No form pages found")
        self.assertIsNone(ret["results"][0]["app_name"])
        self.assertIsNone(ret["results"][0]["class_name"])
        self.assertIsNone(ret["results"][0]["editor_url"])
        self.assertIsNone(ret["results"][0]["url"])

    def test_model_admin_types_serializer(self):
        ret = model_admin_types_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 1)
        self.assertEqual(ret["results"][0]["title"], "No modeladmin models found")
        self.assertIsNone(ret["results"][0]["app_name"])
        self.assertIsNone(ret["results"][0]["class_name"])
        self.assertIsNone(ret["results"][0]["editor_url"])
        self.assertIsNone(ret["results"][0]["url"])

    def test_wagtail_core_edit_pages_serializer(self):
        ret = wagtail_core_edit_pages_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 5)

    def test_wagtail_core_listing_pages_serializer(self):
        ret = wagtail_core_listing_pages_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 16)

    def test_page_model_types_serializer(self):
        ret = page_model_types_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 1)
        self.assertEqual(ret["results"][0]["title"], "No page models found")
        self.assertIsNone(ret["results"][0]["app_name"])
        self.assertIsNone(ret["results"][0]["class_name"])
        self.assertIsNone(ret["results"][0]["editor_url"])
        self.assertIsNone(ret["results"][0]["url"])

    def test_settings_types_serializer(self):
        ret = settings_types_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 1)
        self.assertEqual(
            ret["results"][0]["title"], "wagtail.contrib.settings not in INSTALLED_APPS"
        )
        self.assertIsNone(ret["results"][0]["app_name"])
        self.assertIsNone(ret["results"][0]["class_name"])
        self.assertIsNone(ret["results"][0]["editor_url"])
        self.assertIsNone(ret["results"][0]["url"])

    @override_settings(INSTALLED_APPS=INSTALLED_APPS + ["wagtail.contrib.settings"])
    def test_settings_types_serializer_with_settings(self):
        ret = settings_types_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 1)
        self.assertEqual(ret["results"][0]["title"], "No settings found")
        self.assertIsNone(ret["results"][0]["app_name"])
        self.assertIsNone(ret["results"][0]["class_name"])
        self.assertIsNone(ret["results"][0]["editor_url"])
        self.assertIsNone(ret["results"][0]["url"])

    def test_snippet_types_serializer(self):
        ret = snippet_types_serializer(self.client, "Test")
        self.assertEqual(ret["meta"]["title"], "Test")
        self.assertEqual(len(ret["results"]), 1)
        self.assertEqual(ret["results"][0]["title"], "No snippets found")
        self.assertIsNone(ret["results"][0]["app_name"])
        self.assertIsNone(ret["results"][0]["class_name"])
        self.assertIsNone(ret["results"][0]["editor_url"])
        self.assertIsNone(ret["results"][0]["url"])
