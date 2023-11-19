import logging

from io import StringIO
from sys import stderr

from django.core.management import call_command
from django.test import LiveServerTestCase, TestCase, override_settings
from wagtail import VERSION as WAGTAIL_VERSION


class TestE2ELoadFixtures(TestCase):
    def test_load_fixtures(self):
        args = []
        opts = {}

        with StringIO() as out:
            call_command("load_fixtures", *args, **opts, stdout=out, stderr=stderr)
            output = out.getvalue().strip()
            print(output)  # Just for debugging

        expected = [
            "Creating superuser.",
            "Updating home page.",
            "Creating standard pages.",
            "Creating snippets.",
            "Creating model admins.",
            "Creating settings.",
            "Creating collections.",
            "Creating redirects.",
            "Creating promoted searches.",
            "Importing media files.",
        ]

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)


@override_settings(DEBUG=True)
class TestE2EAdminContentTypes(TestCase):
    def setUp(self):
        with StringIO() as out:
            call_command("load_fixtures", stdout=out, stderr=stderr)

    # @patch(
    #     "wagtail_devtools.management.commands._base_content_types.input",
    #     return_value=28,
    # )
    def test_console_out(self):
        args = []
        opts = {
            "cid": 28,
        }

        with StringIO() as out:
            call_command(
                "cmd_test_content_types", *args, **opts, stdout=out, stderr=out
            )
            output = out.getvalue().strip()

        expected = [
            "Using this command:",
            "Enter a C-Type ID from the list below",
            "to view a report of all the admin edit pages of that type.",
            "Index of Page Types",
            "---------------------------------------------------------------------------------",
            "Model                       App                         C-Type ID",
            "---------------------------------------------------------------------------------",
            "HomePage                    wagtail_devtools_test       3",
            "StandardPageOne             wagtail_devtools_test       28",
            "StandardPageTwo             wagtail_devtools_test       30",
            "StandardPageThree           wagtail_devtools_test       29",
            "---------------------------------------------------------------------------------",
            "Index of Snippet Types",
            "---------------------------------------------------------------------------------",
            "Model                       App                         C-Type ID",
            "---------------------------------------------------------------------------------",
            "TestSnippetOne              wagtail_devtools_test       42",
            "TestSnippetThree            wagtail_devtools_test       40",
            "TestSnippetTwo              wagtail_devtools_test       41",
            "---------------------------------------------------------------------------------",
            "Index of ModelAdmin Types",
            "---------------------------------------------------------------------------------",
            "Model                       App                         C-Type ID",
            "---------------------------------------------------------------------------------",
            "TestModelAdminOne           wagtail_devtools_test       33",
            "TestModelAdminTwo           wagtail_devtools_test       32",
            "TestModelAdminThree         wagtail_devtools_test       31",
            "---------------------------------------------------------------------------------",
            "Index of Settings Types",
            "---------------------------------------------------------------------------------",
            "Model                       App                         C-Type ID",
            "---------------------------------------------------------------------------------",
            "GenericSettingOne           wagtail_devtools_test       38",
            "GenericSettingTwo           wagtail_devtools_test       35",
            "GenericSettingThree         wagtail_devtools_test       34",
            "SiteSettingOne              wagtail_devtools_test       39",
            "SiteSettingTwo              wagtail_devtools_test       36",
            "SiteSettingThree            wagtail_devtools_test       37",
            "---------------------------------------------------------------------------------",
            "Edit Links for StandardPageOne",
            "----------------------------------------------------------------------",
            "Standard Page One",
            "http://localhost:8000/admin/pages/4/edit/",
        ]

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)


@override_settings(DEBUG=True)
class TestE2EAdminResponses(LiveServerTestCase):
    def setUp(self):
        with StringIO() as out:
            call_command("load_fixtures", stdout=out, stderr=stderr)

    def test_console_out(self):
        args = [
            "superuser",
            "superuser",
        ]
        opts = {
            "host": self.live_server_url,
        }
        logging.disable(logging.CRITICAL)

        with StringIO() as out:
            call_command(
                "cmd_test_admin_responses", *args, **opts, stdout=out, stderr=out
            )
            output = out.getvalue().strip()
            print(output)  # Just for debugging

        if WAGTAIL_VERSION >= (5, 2):
            expected = [
                "Checking the admin and frontend responses of 4 page types ...",
                "==============================================================",
                " 1. HomePage",
                " 2. StandardPageOne",
                " 3. StandardPageThree",
                " 4. StandardPageTwo",
                "Home Page ( HomePage ) ↓",
                f"{self.live_server_url}/admin/pages/3/edit/ ← 200",
                f"{self.live_server_url}/ ← 200",
                "Standard Page One ( StandardPageOne ) ↓",
                f"{self.live_server_url}/admin/pages/4/edit/ ← 200",
                f"{self.live_server_url}/standard-page-one/ ← 200",
                "Standard Page Two ( StandardPageTwo ) ↓",
                f"{self.live_server_url}/admin/pages/5/edit/ ← 200",
                f"{self.live_server_url}/standard-page-two/ ← 404 probably a draft page",
                "Standard Page Three ( StandardPageThree ) ↓",
                f"{self.live_server_url}/admin/pages/6/edit/ ← 200",
                f"{self.live_server_url}/standard-page-three/ ← 500",
                "DASHBOARD page ...",
                "===================",
                f"{self.live_server_url}/admin/ ← 200",
                "PAGES list page ...",
                "====================",
                f"{self.live_server_url}/admin/pages/ ← 200",
                "SEARCH all page ...",
                "====================",
                f"{self.live_server_url}/admin/pages/search/ ← 200",
                "AGING PAGES list page ...",
                "==========================",
                f"{self.live_server_url}/admin/reports/aging-pages/ ← 200",
                "COLLECTIONS list page ...",
                "==========================",
                f"{self.live_server_url}/admin/collections/ ← 200",
                "COLLECTIONS EDIT page ...",
                "==========================",
                "Test Collection 1 ↓",
                f"{self.live_server_url}/admin/collections/2/ ← 200",
                "DOCUMENTS list page ...",
                "========================",
                f"{self.live_server_url}/admin/documents/ ← 200",
                "DOCUMENTS edit page ...",
                "========================",
                "Document ↓",
                f"{self.live_server_url}/admin/documents/edit/1/ ← 200",
                "GROUPS list page ...",
                "=====================",
                f"{self.live_server_url}/admin/groups/ ← 200",
                "GROUPS EDIT page ...",
                "=====================",
                "Group ↓",
                f"{self.live_server_url}/admin/groups/edit/1/ ← 200",
                "IMAGES list page ...",
                "=====================",
                f"{self.live_server_url}/admin/images/ ← 200",
                "IMAGES edit page ...",
                "=====================",
                "Image ↓",
                f"{self.live_server_url}/admin/images/1/ ← 200",
                "LOCKED PAGES list page ...",
                "===========================",
                f"{self.live_server_url}/admin/reports/locked/ ← 200",
                "REDIRECTS list page ...",
                "========================",
                f"{self.live_server_url}/admin/redirects/ ← 200",
                "REDIRECTS edit page ...",
                "========================",
                "Redirect ↓",
                f"{self.live_server_url}/admin/redirects/1/ ← 200",
                "SETTINGS edit pages ...",
                "========================",
                "Generic setting one ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/genericsettingone/1/ ← 200",
                "Generic setting two ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/genericsettingtwo/1/ ← 200",
                "Generic setting three ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/genericsettingthree/1/ ← 200",
                "Site setting one ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/sitesettingone/2/ ← 200",
                "Site setting two ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/sitesettingtwo/2/ ← 200",
                "Site setting three ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/sitesettingthree/2/ ← 200",
                "SITES list page ...",
                "====================",
                f"{self.live_server_url}/admin/sites/ ← 200",
                "SITES EDIT page ...",
                "====================",
                "Site ↓",
                f"{self.live_server_url}/admin/sites/edit/2/ ← 200",
                "SITE HISTORY list page ...",
                "===========================",
                f"{self.live_server_url}/admin/reports/site-history/ ← 200",
                "SNIPPETS list page ...",
                "=======================",
                f"{self.live_server_url}/admin/snippets/ ← 200",
                "SNIPPETS models edit pages ...",
                "===============================",
                "Test snippet one ↓",
                f"{self.live_server_url}/admin/snippets/wagtail_devtools_test/testsnippetone/edit/1/ ← 200",
                "Test snippet three ↓",
                f"{self.live_server_url}/admin/snippets/wagtail_devtools_test/testsnippetthree/edit/1/ ← 200",
                "Test snippet two ↓",
                f"{self.live_server_url}/admin/snippets/wagtail_devtools_test/testsnippettwo/edit/1/ ← 200",
                "USERS list page ...",
                "====================",
                f"{self.live_server_url}/admin/users/ ← 200",
                "USERS EDIT page ...",
                "====================",
                "User ↓",
                f"{self.live_server_url}/admin/users/1/ ← 200",
                "WORKFLOWS list page ...",
                "========================",
                f"{self.live_server_url}/admin/workflows/list/ ← 200",
                "WORKFLOWS edit page ...",
                "========================",
                "Workflow ↓",
                f"{self.live_server_url}/admin/workflows/edit/1/ ← 200",
                "WORKFLOWS TASKS list page ...",
                "==============================",
                f"{self.live_server_url}/admin/workflows/tasks/index/ ← 200",
                "WORKFLOWS TASK edit page ...",
                "=============================",
                "Task ↓",
                f"{self.live_server_url}/admin/workflows/tasks/edit/1/ ← 200",
            ]
        else:
            # Groups and sites url don't use the /edit/ path below 5.2
            expected = [
                "Checking the admin and frontend responses of 4 page types ...",
                "==============================================================",
                " 1. HomePage",
                " 2. StandardPageOne",
                " 3. StandardPageThree",
                " 4. StandardPageTwo",
                "Home Page ( HomePage ) ↓",
                f"{self.live_server_url}/admin/pages/3/edit/ ← 200",
                f"{self.live_server_url}/ ← 200",
                "Standard Page One ( StandardPageOne ) ↓",
                f"{self.live_server_url}/admin/pages/4/edit/ ← 200",
                f"{self.live_server_url}/standard-page-one/ ← 200",
                "Standard Page Two ( StandardPageTwo ) ↓",
                f"{self.live_server_url}/admin/pages/5/edit/ ← 200",
                f"{self.live_server_url}/standard-page-two/ ← 404 probably a draft page",
                "Standard Page Three ( StandardPageThree ) ↓",
                f"{self.live_server_url}/admin/pages/6/edit/ ← 200",
                f"{self.live_server_url}/standard-page-three/ ← 500",
                "DASHBOARD page ...",
                "===================",
                f"{self.live_server_url}/admin/ ← 200",
                "PAGES list page ...",
                "====================",
                f"{self.live_server_url}/admin/pages/ ← 200",
                "SEARCH all page ...",
                "====================",
                f"{self.live_server_url}/admin/pages/search/ ← 200",
                "AGING PAGES list page ...",
                "==========================",
                f"{self.live_server_url}/admin/reports/aging-pages/ ← 200",
                "COLLECTIONS list page ...",
                "==========================",
                f"{self.live_server_url}/admin/collections/ ← 200",
                "COLLECTIONS EDIT page ...",
                "==========================",
                "Test Collection 1 ↓",
                f"{self.live_server_url}/admin/collections/2/ ← 200",
                "DOCUMENTS list page ...",
                "========================",
                f"{self.live_server_url}/admin/documents/ ← 200",
                "DOCUMENTS edit page ...",
                "========================",
                "Document ↓",
                f"{self.live_server_url}/admin/documents/edit/1/ ← 200",
                "GROUPS list page ...",
                "=====================",
                f"{self.live_server_url}/admin/groups/ ← 200",
                "GROUPS EDIT page ...",
                "=====================",
                "Group ↓",
                f"{self.live_server_url}/admin/groups/1/ ← 200",
                "IMAGES list page ...",
                "=====================",
                f"{self.live_server_url}/admin/images/ ← 200",
                "IMAGES edit page ...",
                "=====================",
                "Image ↓",
                f"{self.live_server_url}/admin/images/1/ ← 200",
                "LOCKED PAGES list page ...",
                "===========================",
                f"{self.live_server_url}/admin/reports/locked/ ← 200",
                "REDIRECTS list page ...",
                "========================",
                f"{self.live_server_url}/admin/redirects/ ← 200",
                "REDIRECTS edit page ...",
                "========================",
                "Redirect ↓",
                f"{self.live_server_url}/admin/redirects/1/ ← 200",
                "SETTINGS edit pages ...",
                "========================",
                "Generic setting one ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/genericsettingone/1/ ← 200",
                "Generic setting two ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/genericsettingtwo/1/ ← 200",
                "Generic setting three ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/genericsettingthree/1/ ← 200",
                "Site setting one ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/sitesettingone/2/ ← 200",
                "Site setting two ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/sitesettingtwo/2/ ← 200",
                "Site setting three ↓",
                f"{self.live_server_url}/admin/settings/wagtail_devtools_test/sitesettingthree/2/ ← 200",
                "SITES list page ...",
                "====================",
                f"{self.live_server_url}/admin/sites/ ← 200",
                "SITES EDIT page ...",
                "====================",
                "Site ↓",
                f"{self.live_server_url}/admin/sites/2/ ← 200",
                "SITE HISTORY list page ...",
                "===========================",
                f"{self.live_server_url}/admin/reports/site-history/ ← 200",
                "SNIPPETS list page ...",
                "=======================",
                f"{self.live_server_url}/admin/snippets/ ← 200",
                "SNIPPETS models edit pages ...",
                "===============================",
                "Test snippet one ↓",
                f"{self.live_server_url}/admin/snippets/wagtail_devtools_test/testsnippetone/edit/1/ ← 200",
                "Test snippet three ↓",
                f"{self.live_server_url}/admin/snippets/wagtail_devtools_test/testsnippetthree/edit/1/ ← 200",
                "Test snippet two ↓",
                f"{self.live_server_url}/admin/snippets/wagtail_devtools_test/testsnippettwo/edit/1/ ← 200",
                "USERS list page ...",
                "====================",
                f"{self.live_server_url}/admin/users/ ← 200",
                "USERS EDIT page ...",
                "====================",
                "User ↓",
                f"{self.live_server_url}/admin/users/1/ ← 200",
                "WORKFLOWS list page ...",
                "========================",
                f"{self.live_server_url}/admin/workflows/list/ ← 200",
                "WORKFLOWS edit page ...",
                "========================",
                "Workflow ↓",
                f"{self.live_server_url}/admin/workflows/edit/1/ ← 200",
                "WORKFLOWS TASKS list page ...",
                "==============================",
                f"{self.live_server_url}/admin/workflows/tasks/index/ ← 200",
                "WORKFLOWS TASK edit page ...",
                "=============================",
                "Task ↓",
                f"{self.live_server_url}/admin/workflows/tasks/edit/1/ ← 200",
            ]

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)
