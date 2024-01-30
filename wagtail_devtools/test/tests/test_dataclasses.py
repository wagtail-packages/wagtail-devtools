from django.test import RequestFactory, TestCase, override_settings

from wagtail_devtools.api.dataclasses import (
    Results,
    ResultsListingItem,
    ResultsModelItem,
)
from wagtail_devtools.test.models import HomePage


class TestResultsModelItem(TestCase):
    def test_results_model_item(self):
        request = RequestFactory().get("/")
        item = HomePage.objects.first()
        results_model_item = ResultsModelItem(request, item)
        self.assertEqual(
            results_model_item.get(),
            {
                "title": "Home",
                "app_name": "wagtail_devtools_test",
                "class_name": "HomePage",
                "editor_url": "http://localhost:8000/admin/pages/3/edit/",
                "url": "/",
            },
        )

    @override_settings(DEVTOOLS_FIELD_IDENTIFIER=[])
    def test_results_model_item_no_title_field(self):
        request = RequestFactory().get("/")
        item = HomePage.objects.first()
        del item.title
        results_model_item = ResultsModelItem(request, item)
        self.assertEqual(results_model_item.title, "Title Field not found")


class TestResultsListingItem(TestCase):
    def test_results_listing_item(self):
        request = RequestFactory().get("/")
        item = {
            "title": "Search promotions",
            "app_name": "wagtailsearchpromotions",
            "listing_name": "wagtailsearchpromotions:index",
        }
        results_listing_item = ResultsListingItem(request, item)
        self.assertEqual(
            results_listing_item.get(),
            {
                "title": "Search promotions",
                "app_name": "wagtailsearchpromotions",
                "class_name": None,
                "editor_url": "http://localhost:8000/admin/searchpicks/",
                "url": None,
            },
        )


class TestResults(TestCase):
    def test_results(self):
        results = Results()
        self.assertEqual(results.items, [])

    def test_results_items_list(self):
        result = ResultsListingItem(
            RequestFactory().get("/"),
            {
                "title": "Search promotions",
                "app_name": "wagtailsearchpromotions",
                "listing_name": "wagtailsearchpromotions:index",
            },
        ).get()
        results = Results()
        results.add(result)
        self.assertEqual(
            results.items,
            [
                {
                    "title": "Search promotions",
                    "app_name": "wagtailsearchpromotions",
                    "class_name": None,
                    "editor_url": "http://localhost:8000/admin/searchpicks/",
                    "url": None,
                }
            ],
        )
        results.add(result)
        self.assertEqual(
            results.items,
            [
                {
                    "title": "Search promotions",
                    "app_name": "wagtailsearchpromotions",
                    "class_name": None,
                    "editor_url": "http://localhost:8000/admin/searchpicks/",
                    "url": None,
                }
            ],
        )
        r = results.get()
        self.assertEqual(
            r,
            [
                {
                    "title": "Search promotions",
                    "app_name": "wagtailsearchpromotions",
                    "class_name": None,
                    "editor_url": "http://localhost:8000/admin/searchpicks/",
                    "url": None,
                }
            ],
        )
