from unittest.mock import patch

from django.test import RequestFactory, TestCase
from wagtail.models import Collection, Group
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.conf import (
    get_wagtail_core_edit_pages_config,
    get_wagtail_core_listing_pages_config,
)
from wagtail_devtools.api.helpers import get_admin_edit_url
from wagtail_devtools.api.serializers import (
    wagtail_core_apps_serializer,
    wagtail_core_listing_pages_serializer,
)
from wagtail_devtools.test.models import HomePage


class TestWagtailCoreListingPageSerializer(TestCase):
    @patch("wagtail_devtools.api.conf.get_listing_pages_config")
    def test_wagtail_core_listing_page_serializer(self, mock_listing_pages_config):
        mock_listing_pages_config.return_value = [
            {
                "title": "Search promotions",
                "app_name": "wagtailsearchpromotions",
                "listing_name": "wagtailsearchpromotions:index",
            }
        ]
        config = get_wagtail_core_listing_pages_config()
        request = RequestFactory().get("/")
        ret = wagtail_core_listing_pages_serializer(request, config, "title")
        expected = {
            "meta": {"title": "title"},
            "results": [
                {
                    "title": "Search promotions",
                    "app_name": "wagtailsearchpromotions",
                    "class_name": None,
                    "editor_url": "http://localhost:8000/admin/searchpicks/",
                    "url": None,
                }
            ],
        }
        self.assertEqual(ret, expected)


class TestWagtailCoreAppsSerializer(TestCase):
    @patch("wagtail_devtools.api.conf.get_wagtail_core_edit_pages_config")
    def test_wagtail_core_apps_serializer(self, mock_edit_pages_config):
        mock_edit_pages_config.return_value = {
            "title": "Wagtail core apps",
            "apps": [
                {
                    "app_name": "wagtail.core",
                    "models": [
                        {
                            "model_name": "Page",
                            "fields": ["title", "slug", "seo_title", "show_in_menus"],
                        }
                    ],
                }
            ],
        }
        config = get_wagtail_core_edit_pages_config()
        request = RequestFactory().get("/")
        ret = wagtail_core_apps_serializer(request, config, "title")

        # editor_url is different in different versions of wagtail
        # so need to get the correct expected value for editor_url
        home_page = HomePage.objects.get(slug="home")
        editor_url = get_admin_edit_url(request, home_page)

        self.assertEqual(len(ret["results"]), 6)
        self.assertEqual(ret["results"][0]["title"], "Home")
        self.assertEqual(ret["results"][0]["app_name"], "wagtail_devtools_test")
        self.assertEqual(ret["results"][0]["class_name"], "HomePage")
        self.assertEqual(ret["results"][0]["editor_url"], editor_url)

        # editor_url is different in different versions of wagtail
        # so need to get the correct expected value for editor_url
        group = Group.objects.get(name="Moderators")
        editor_url = get_admin_edit_url(request, group)

        self.assertEqual(ret["results"][5]["title"], "Moderators")
        self.assertEqual(ret["results"][5]["app_name"], "auth")
        self.assertEqual(ret["results"][5]["class_name"], "Group")
        self.assertEqual(ret["results"][5]["editor_url"], editor_url)

    def test_wagtail_core_apps_serializer_with_all(self):
        config = get_wagtail_core_edit_pages_config()
        request = RequestFactory().get("/")
        ret = wagtail_core_apps_serializer(request, config, "title", all=True)
        self.assertEqual(len(ret["results"]), 7)

    def test_wagtail_core_apps_serializer_with_collection(self):
        # create a collection
        root_collection = Collection.objects.first()
        root_collection.add_child(name="Test Collection")
        collection = Collection.objects.get(name="Test Collection")
        collection_edit_url = get_admin_edit_url("http://localhost:8000", collection)

        # create a snippet
        model = get_snippet_models()[0]
        snippet = model.objects.create(title="test snippet")
        snippet.save()
        snippet_edit_url = get_admin_edit_url("http://localhost:8000", snippet)

        config = get_wagtail_core_edit_pages_config()
        request = RequestFactory().get("/")
        ret = wagtail_core_apps_serializer(request, config, "title", all=True)

        self.assertEqual(ret["results"][3]["title"], "Test Collection")
        self.assertEqual(ret["results"][3]["app_name"], "wagtailcore")
        self.assertEqual(ret["results"][3]["class_name"], "Collection")
        self.assertEqual(ret["results"][3]["editor_url"], collection_edit_url)

        self.assertEqual(ret["results"][1]["title"], "test snippet")
        self.assertEqual(ret["results"][1]["app_name"], "wagtail_devtools_test")
        self.assertEqual(ret["results"][1]["class_name"], "TestSnippetOne")
        self.assertEqual(ret["results"][1]["editor_url"], snippet_edit_url)
