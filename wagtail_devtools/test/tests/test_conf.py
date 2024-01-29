from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_devtools.api.conf import (
    get_wagtail_core_edit_pages_config,
    get_wagtail_core_listing_pages_config,
)


class TestApiConf(SimpleTestCase):
    """Test the API conf."""

    def test_wagtail_core_listing_pages_config(self):
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
            {
                "title": "Example Calendar (admin view)",
                "app_name": None,
                "listing_name": "calendar",
            },
            {
                "title": "Example Calendar (admin view - month)",
                "app_name": None,
                "listing_name": "calendar-month",
            },
        ]

        self.assertEqual(conf["apps"], expected_apps)

    @override_settings(DEVTOOLS_LISTING_EXCLUDE=["wagtailsearchpromotions:index"])
    def test_wagtail_core_listing_pages_config_exclude_one(self):
        conf = get_wagtail_core_listing_pages_config()
        self.assertEqual(
            conf["apps"][0]["title"], "Forms"
        )  # not "Search promotions" as first item

    @override_settings(
        DEVTOOLS_LISTING_EXCLUDE=["wagtailsearchpromotions:index", "wagtailforms:index"]
    )
    def test_wagtail_core_listing_pages_config_exclude_multiple(self):
        conf = get_wagtail_core_listing_pages_config()
        self.assertEqual(
            conf["apps"][0]["title"], "Redirects"
        )  # not "Search promotions" as first item

    @patch("wagtail_devtools.api.conf.get_listing_pages_config")
    def test_not_appear_in_listing(self, mock_listing_pages_config):
        mock_listing_pages_config.return_value = [
            {
                "title": "Search promotions",
                "app_name": "wagtailsearchpromotions",
                "listing_name": None,
            },
        ]
        conf = get_wagtail_core_listing_pages_config()
        self.assertEqual(conf["apps"], [])

    def test_get_wagtail_core_edit_pages_config(self):
        conf = get_wagtail_core_edit_pages_config()
        self.assertEqual(conf["title"], "Wagtail core edit pages")
        self.assertIsInstance(conf["apps"], list)

        if WAGTAIL_VERSION >= (5, 0):
            expected = [
                {"app_name": "wagtail_devtools", "models": []},
                {
                    "app_name": "wagtail_devtools_test",
                    "models": [
                        "HomePage",
                        "SecondHomePage",
                        "StandardPageOne",
                        "StandardPageTwo",
                        "StandardPageThree",
                        "FormFieldOne",
                        "FormPageOne",
                        "FormFieldTwo",
                        "FormPageTwo",
                        "TestSnippetOne",
                        "TestSnippetTwo",
                        "TestSnippetThree",
                        "TestModelAdminOne",
                        "TestModelAdminTwo",
                        "TestModelAdminThree",
                        "GenericSettingOne",
                        "GenericSettingTwo",
                        "GenericSettingThree",
                        "SiteSettingOne",
                        "SiteSettingTwo",
                        "SiteSettingThree",
                        "FrontendPage500",
                        "FrontendPage404",
                        "FrontendPage302",
                        "FrontendPage200",
                    ],
                },
                {
                    "app_name": "wagtailsearchpromotions",
                    "models": ["Query", "QueryDailyHits", "SearchPromotion"],
                },
                {"app_name": "wagtailforms", "models": ["FormSubmission"]},
                {"app_name": "wagtailredirects", "models": ["Redirect"]},
                {"app_name": "wagtailsettings", "models": []},
                {"app_name": "wagtailembeds", "models": ["Embed"]},
                {"app_name": "wagtailusers", "models": ["UserProfile"]},
                {"app_name": "wagtailsnippets", "models": []},
                {"app_name": "wagtaildocs", "models": ["Document", "UploadedDocument"]},
                {
                    "app_name": "wagtailimages",
                    "models": ["Image", "Rendition", "UploadedImage"],
                },
                {
                    "app_name": "wagtailsearch",
                    "models": [
                        "Query",
                        "QueryDailyHits",
                        "SQLiteFTSIndexEntry",
                        "IndexEntry",
                    ],
                },
                {"app_name": "wagtailadmin", "models": ["Admin"]},
                {"app_name": "wagtailapi_v2", "models": []},
                {"app_name": "wagtailmodeladmin", "models": []},
                {"app_name": "wagtailroutablepage", "models": []},
                {"app_name": "wagtailstyleguide", "models": []},
                {"app_name": "wagtailsites", "models": []},
                {
                    "app_name": "wagtailcore",
                    "models": [
                        "Locale",
                        "Site",
                        "ModelLogEntry",
                        "CollectionViewRestriction_groups",
                        "CollectionViewRestriction",
                        "Collection",
                        "GroupCollectionPermission",
                        "ReferenceIndex",
                        "Page",
                        "Revision",
                        "GroupPagePermission",
                        "PageViewRestriction_groups",
                        "PageViewRestriction",
                        "WorkflowPage",
                        "WorkflowContentType",
                        "WorkflowTask",
                        "Task",
                        "Workflow",
                        "GroupApprovalTask_groups",
                        "GroupApprovalTask",
                        "WorkflowState",
                        "TaskState",
                        "PageLogEntry",
                        "Comment",
                        "CommentReply",
                        "PageSubscription",
                    ],
                },
                {"app_name": "taggit", "models": ["Tag", "TaggedItem"]},
                {"app_name": "rest_framework", "models": []},
                {"app_name": "admin", "models": ["LogEntry"]},
                {
                    "app_name": "auth",
                    "models": [
                        "Permission",
                        "Group_permissions",
                        "Group",
                        "User_groups",
                        "User_user_permissions",
                        "User",
                    ],
                },
                {"app_name": "contenttypes", "models": ["ContentType"]},
                {"app_name": "sessions", "models": ["Session"]},
                {"app_name": "messages", "models": []},
                {"app_name": "staticfiles", "models": []},
                {"app_name": "sitemaps", "models": []},
            ]
        else:
            expected = [
                {"app_name": "wagtail_devtools", "models": []},
                {
                    "app_name": "wagtail_devtools_test",
                    "models": [
                        "HomePage",
                        "SecondHomePage",
                        "StandardPageOne",
                        "StandardPageTwo",
                        "StandardPageThree",
                        "FormFieldOne",
                        "FormPageOne",
                        "FormFieldTwo",
                        "FormPageTwo",
                        "TestSnippetOne",
                        "TestSnippetTwo",
                        "TestSnippetThree",
                        "TestModelAdminOne",
                        "TestModelAdminTwo",
                        "TestModelAdminThree",
                        "GenericSettingOne",
                        "GenericSettingTwo",
                        "GenericSettingThree",
                        "SiteSettingOne",
                        "SiteSettingTwo",
                        "SiteSettingThree",
                        "FrontendPage500",
                        "FrontendPage404",
                        "FrontendPage302",
                        "FrontendPage200",
                    ],
                },
                {"app_name": "wagtailsearchpromotions", "models": ["SearchPromotion"]},
                {"app_name": "wagtailforms", "models": ["FormSubmission"]},
                {"app_name": "wagtailredirects", "models": ["Redirect"]},
                {"app_name": "wagtailsettings", "models": []},
                {"app_name": "wagtailembeds", "models": ["Embed"]},
                {"app_name": "wagtailusers", "models": ["UserProfile"]},
                {"app_name": "wagtailsnippets", "models": []},
                {"app_name": "wagtaildocs", "models": ["Document", "UploadedDocument"]},
                {
                    "app_name": "wagtailimages",
                    "models": ["Image", "Rendition", "UploadedImage"],
                },
                {
                    "app_name": "wagtailsearch",
                    "models": [
                        "Query",
                        "QueryDailyHits",
                        "SQLiteFTSIndexEntry",
                        "IndexEntry",
                    ],
                },
                {"app_name": "wagtailadmin", "models": ["Admin"]},
                {"app_name": "wagtailapi_v2", "models": []},
                {"app_name": "wagtailmodeladmin", "models": []},
                {"app_name": "wagtailroutablepage", "models": []},
                {"app_name": "wagtailstyleguide", "models": []},
                {"app_name": "wagtailsites", "models": []},
                {
                    "app_name": "wagtailcore",
                    "models": [
                        "Locale",
                        "Site",
                        "ModelLogEntry",
                        "CollectionViewRestriction_groups",
                        "CollectionViewRestriction",
                        "Collection",
                        "GroupCollectionPermission",
                        "ReferenceIndex",
                        "Page",
                        "Revision",
                        "GroupPagePermission",
                        "PageViewRestriction_groups",
                        "PageViewRestriction",
                        "WorkflowPage",
                        "WorkflowContentType",
                        "WorkflowTask",
                        "Task",
                        "Workflow",
                        "GroupApprovalTask_groups",
                        "GroupApprovalTask",
                        "WorkflowState",
                        "TaskState",
                        "PageLogEntry",
                        "Comment",
                        "CommentReply",
                        "PageSubscription",
                    ],
                },
                {"app_name": "taggit", "models": ["Tag", "TaggedItem"]},
                {"app_name": "rest_framework", "models": []},
                {"app_name": "admin", "models": ["LogEntry"]},
                {
                    "app_name": "auth",
                    "models": [
                        "Permission",
                        "Group_permissions",
                        "Group",
                        "User_groups",
                        "User_user_permissions",
                        "User",
                    ],
                },
                {"app_name": "contenttypes", "models": ["ContentType"]},
                {"app_name": "sessions", "models": ["Session"]},
                {"app_name": "messages", "models": []},
                {"app_name": "staticfiles", "models": []},
                {"app_name": "sitemaps", "models": []},
            ]

        self.assertEqual(conf["apps"], expected)

    @override_settings(DEVTOOLS_APPS_EXCLUDE=["wagtail_devtools"])
    def test_wagtail_core_edit_pages_config_exclude_one(self):
        conf = get_wagtail_core_edit_pages_config()
        self.assertEqual(
            conf["apps"][0]["app_name"], "wagtail_devtools_test"
        )  # not "wagtail_devtools" as first item
