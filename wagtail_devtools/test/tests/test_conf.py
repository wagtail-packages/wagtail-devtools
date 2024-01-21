from django.conf import settings
from django.test import SimpleTestCase, override_settings

from wagtail_devtools.api.conf import (
    get_registered_modeladmin,
    wagtail_core_edit_pages_config,
    wagtail_core_listing_pages_config,
)


class TestApiConf(SimpleTestCase):
    """Test the API conf."""

    @override_settings(WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES=[])
    def test_model_admin_types(self):
        # simulate the absence of the setting
        del settings.WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES
        self.assertEqual(get_registered_modeladmin(), [])

    @override_settings(WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES=[])
    def test_get_model_admin_types_empty(self):
        # There's no default value for this setting
        self.assertEqual(get_registered_modeladmin(), [])

    @override_settings(WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES=["test"])
    def test_get_model_admin_types_with_value(self):
        self.assertEqual(get_registered_modeladmin(), ["test"])

    @override_settings(WAGTAIL_DEVTOOLS_EDIT_PAGES=[])
    def test_wagtail_core_edit_pages_config(self):
        # simulate the absence of the setting
        del settings.WAGTAIL_DEVTOOLS_EDIT_PAGES
        self.assertIn("auth.User", wagtail_core_edit_pages_config())
        self.assertIn("auth.Group", wagtail_core_edit_pages_config())
        self.assertIn("wagtailcore.Collection", wagtail_core_edit_pages_config())
        self.assertIn("wagtailcore.Site", wagtail_core_edit_pages_config())
        self.assertIn("wagtailcore.Task", wagtail_core_edit_pages_config())
        self.assertIn("wagtailcore.Workflow", wagtail_core_edit_pages_config())
        self.assertIn("wagtaildocs.Document", wagtail_core_edit_pages_config())
        self.assertIn("wagtailimages.Image", wagtail_core_edit_pages_config())
        self.assertIn("wagtailredirects.Redirect", wagtail_core_edit_pages_config())

    @override_settings(WAGTAIL_DEVTOOLS_EDIT_PAGES=["test.Model"])
    def test_wagtail_core_edit_pages_config_with_value(self):
        self.assertEqual(
            wagtail_core_edit_pages_config(),
            ["test.Model"],
        )

    @override_settings(WAGTAIL_DEVTOOLS_LISTING_PAGES=[])
    def test_wagtail_core_listing_pages_config(self):
        # simulate the absence of the setting
        del settings.WAGTAIL_DEVTOOLS_LISTING_PAGES
        self.assertEqual(
            wagtail_core_listing_pages_config(),
            [
                "wagtailadmin_collections:index",
                "wagtailadmin_explore_root",
                "wagtailadmin_home",
                "wagtailadmin_pages:search",
                "wagtailadmin_reports:aging_pages",
                "wagtailadmin_reports:locked_pages",
                "wagtailadmin_reports:site_history",
                "wagtailadmin_workflows:index",
                "wagtailadmin_workflows:task_index",
                "wagtaildocs:index",
                "wagtailimages:index",
                "wagtailredirects:index",
                "wagtailsites:index",
                "wagtailsnippets:index",
                "wagtailusers_groups:index",
                "wagtailusers_users:index",
            ],
        )

    @override_settings(WAGTAIL_DEVTOOLS_LISTING_PAGES=["test:index"])
    def test_wagtail_core_listing_pages_config_with_value(self):
        self.assertEqual(
            wagtail_core_listing_pages_config(),
            ["test:index"],
        )
