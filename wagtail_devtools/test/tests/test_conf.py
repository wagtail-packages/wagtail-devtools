from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings

from wagtail_devtools.api.conf import (
    get_wagtail_core_edit_pages_config,
    get_wagtail_core_listing_pages_config,
)


class TestListingConf(SimpleTestCase):
    """Tests for the listing pages config."""

    def test_wagtail_core_listing_pages_config(self):
        """Test the default config for wagtail core listing pages.
        This really about what goes in must come out."""

        conf = get_wagtail_core_listing_pages_config()
        self.assertEqual(conf["title"], "Wagtail core listing pages")
        self.assertIsInstance(conf["apps"], list)

        expected_apps = [
            {
                "title": "Search promotions",
                "app_name": "wagtailsearchpromotions",
                "listing_name": "wagtailsearchpromotions:index",
            },
            {
                "title": "Forms",
                "app_name": "wagtailforms",
                "listing_name": "wagtailforms:index",
            },
            {
                "title": "Redirects",
                "app_name": "wagtailredirects",
                "listing_name": "wagtailredirects:index",
            },
            {
                "title": "Users",
                "app_name": "wagtailusers",
                "listing_name": "wagtailusers_users:index",
            },
            {
                "title": "Snippets",
                "app_name": "wagtailsnippets",
                "listing_name": "wagtailsnippets:index",
            },
            {
                "title": "Documents",
                "app_name": "wagtaildocs",
                "listing_name": "wagtaildocs:index",
            },
            {
                "title": "Images",
                "app_name": "wagtailimages",
                "listing_name": "wagtailimages:index",
            },
            {
                "title": "Search",
                "app_name": "wagtailsearch",
                "listing_name": "wagtailadmin_pages:search",
            },
            {
                "title": "Styleguide",
                "app_name": "wagtailstyleguide",
                "listing_name": "wagtailstyleguide",
            },
            {
                "title": "Sites",
                "app_name": "wagtailsites",
                "listing_name": "wagtailsites:index",
            },
            {
                "title": "Dashboard",
                "app_name": None,
                "listing_name": "wagtailadmin_home",
            },
            {
                "title": "Collections",
                "app_name": None,
                "listing_name": "wagtailadmin_collections:index",
            },
            {"title": "Login", "app_name": None, "listing_name": "wagtailadmin_login"},
            {
                "title": "Password reset",
                "app_name": None,
                "listing_name": "wagtailadmin_password_reset",
            },
            {
                "title": "Reports Locked Pages",
                "app_name": None,
                "listing_name": "wagtailadmin_reports:locked_pages",
            },
            {
                "title": "Reports Aging Pages",
                "app_name": None,
                "listing_name": "wagtailadmin_reports:aging_pages",
            },
            {
                "title": "Reports Site History",
                "app_name": None,
                "listing_name": "wagtailadmin_reports:site_history",
            },
            {
                "title": "Reports Workflow",
                "app_name": None,
                "listing_name": "wagtailadmin_reports:workflow",
            },
            {
                "title": "Reports Workflow Tasks",
                "app_name": None,
                "listing_name": "wagtailadmin_reports:workflow_tasks",
            },
            {
                "title": "Reports Workflows",
                "app_name": None,
                "listing_name": "wagtailadmin_workflows:index",
            },
            {
                "title": "Groups",
                "app_name": None,
                "listing_name": "wagtailusers_groups:index",
            },
        ]

        self.assertEqual(conf["apps"], expected_apps)

    @patch("wagtail_devtools.api.conf.LISTING_PAGES_CONFIG")
    def test_wagtail_core_listing_pages_config_missing_list_name(self, mock_config):
        mock_config.append(
            {
                "title": "Example Calendar (admin view - month)",
                "app_name": None,
                "listing_name": None,
            }
        )
        conf = get_wagtail_core_listing_pages_config()
        self.assertIsInstance(conf["apps"], list)
        self.assertEqual(len(conf["apps"]), 0)

    @override_settings(DEVTOOLS_LISTING_EXCLUDE=["wagtailsearchpromotions:index"])
    def test_wagtail_core_listing_pages_config_exclude_one(self):
        """Test the default config for wagtail core listing pages.
        This tests the exclude functionality."""

        conf = get_wagtail_core_listing_pages_config()
        self.assertEqual(
            conf["apps"][0]["title"], "Forms"
        )  # not "Search promotions" as first item

    @override_settings(
        DEVTOOLS_LISTING_EXCLUDE=["wagtailsearchpromotions:index", "wagtailforms:index"]
    )
    def test_wagtail_core_listing_pages_config_exclude_multiple(self):
        """Test the default config for wagtail core listing pages.
        This tests the exclude functionality with multiple exclude items."""

        conf = get_wagtail_core_listing_pages_config()
        self.assertEqual(
            conf["apps"][0]["title"], "Redirects"
        )  # not "Search promotions" as first item


class TestEditConf(TestCase):
    """Tests for the edit pages config."""

    def setUpTestData():
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)

    def test_get_wagtail_core_edit_pages_config(self):
        """Test the default config for wagtail core edit pages.
        Loading all the possible apps we know about that are in the test_app."""

        conf = get_wagtail_core_edit_pages_config()
        self.assertEqual(conf["title"], "Wagtail core edit pages")
        self.assertIsInstance(conf["apps"], list)
        # for app in conf["apps"]:
        #     self.assertIsInstance(app["models"], list)
        #     keys = app.keys()
        #     self.assertIn("app_name", keys)
        #     self.assertIn("models", keys)
        #     self.assertIsInstance(app["models"], list)

        #     # check known models in the test_app
        #     if app["app_name"] == "wagtail_devtools_test":
        #         self.assertEqual(
        #             app,
        #             {
        #                 "app_name": "wagtail_devtools_test",
        #                 "models": [
        #                     "HomePage",
        #                     "SecondHomePage",
        #                     "StandardPageOne",
        #                     "StandardPageTwo",
        #                     "StandardPageThree",
        #                     "FormFieldOne",
        #                     "FormPageOne",
        #                     "FormFieldTwo",
        #                     "FormPageTwo",
        #                     "TestSnippetOne",
        #                     "TestSnippetTwo",
        #                     "TestSnippetThree",
        #                     "TestModelAdminOne",
        #                     "TestModelAdminTwo",
        #                     "TestModelAdminThree",
        #                     "GenericSettingOne",
        #                     "GenericSettingTwo",
        #                     "GenericSettingThree",
        #                     "SiteSettingOne",
        #                     "SiteSettingTwo",
        #                     "SiteSettingThree",
        #                     "FrontendPage500",
        #                     "FrontendPage404",
        #                     "FrontendPage302",
        #                     "FrontendPage200",
        #                 ],
        #             },
        #         )

        #     # check known models in the wagtailcore app
        #     if app["app_name"] == "wagtailcore":
        #         self.assertEqual(
        #             app,
        #             {
        #                 "app_name": "wagtailcore",
        #                 "models": [
        #                     "Locale",
        #                     "Site",
        #                     "ModelLogEntry",
        #                     "CollectionViewRestriction_groups",
        #                     "CollectionViewRestriction",
        #                     "Collection",
        #                     "GroupCollectionPermission",
        #                     "ReferenceIndex",
        #                     "Page",
        #                     "Revision",
        #                     "GroupPagePermission",
        #                     "PageViewRestriction_groups",
        #                     "PageViewRestriction",
        #                     "WorkflowPage",
        #                     "WorkflowContentType",
        #                     "WorkflowTask",
        #                     "Task",
        #                     "Workflow",
        #                     "GroupApprovalTask_groups",
        #                     "GroupApprovalTask",
        #                     "WorkflowState",
        #                     "TaskState",
        #                     "PageLogEntry",
        #                     "Comment",
        #                     "CommentReply",
        #                     "PageSubscription",
        #                 ],
        #             },
        #         )

    @override_settings(DEVTOOLS_APPS_EXCLUDE=["wagtail_devtools"])
    def test_wagtail_core_edit_pages_config_exclude_one(self):
        """Test the default config for wagtail core edit pages.
        This tests the exclude functionality."""

        conf = get_wagtail_core_edit_pages_config()
        for app in conf["apps"]:
            self.assertNotEqual(app["app_name"], "wagtail_devtools")
