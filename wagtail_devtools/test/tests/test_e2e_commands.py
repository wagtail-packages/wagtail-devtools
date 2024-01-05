import logging
import shutil

from io import StringIO
from sys import stderr

from django.conf import settings
from django.core.management import call_command
from django.test import LiveServerTestCase, TestCase, override_settings


class TestE2ELoadFixtures(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)
        super().tearDownClass()

    def test_build_fixtures(self):
        args = [
            "--no-color",
        ]
        opts = {}

        with StringIO() as out:
            call_command("build_fixtures", *args, **opts, stdout=out, stderr=stderr)
            output = out.getvalue().strip()
            # print(output)  # Just for debugging

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
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)
        super().tearDownClass()

    def setUp(self):
        with StringIO() as out:
            call_command("build_fixtures", stdout=out, stderr=stderr)

    def test_console_out(self):
        args = [
            "--no-color",
        ]
        opts = {
            "cid": 3,
        }

        with StringIO() as out:
            call_command(
                "cmd_test_content_types", *args, **opts, stdout=out, stderr=out
            )
            output = out.getvalue().strip()
            print(output)  # Just for debugging

            expected = [  # Not testing for existence of the edit links or cid value as can't be guaranteed
                "Using this command:",
                "Enter a C-Type ID from the list below",
                "to view a report of all the admin edit pages of that type.",
                "Index of Page Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "HomePage                    wagtail_devtools_test",
                "StandardPageOne             wagtail_devtools_test",
                "StandardPageTwo             wagtail_devtools_test",
                "StandardPageThree           wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
                "Index of Snippet Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "TestSnippetOne              wagtail_devtools_test",
                "TestSnippetThree            wagtail_devtools_test",
                "TestSnippetTwo              wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
                "Index of ModelAdmin Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "TestModelAdminOne           wagtail_devtools_test",
                "TestModelAdminTwo           wagtail_devtools_test",
                "TestModelAdminThree         wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
                "Index of Settings Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "GenericSettingOne           wagtail_devtools_test",
                "GenericSettingTwo           wagtail_devtools_test",
                "GenericSettingThree         wagtail_devtools_test",
                "SiteSettingOne              wagtail_devtools_test",
                "SiteSettingTwo              wagtail_devtools_test",
                "SiteSettingThree            wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
            ]

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)


@override_settings(DEBUG=True)
class TestE2EAdminResponses(LiveServerTestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)
        super().tearDownClass()

    def setUp(self):
        print(f"Live server url: {self.live_server_url}")  # Just for debugging
        with StringIO() as out:
            call_command("build_fixtures", stdout=out, stderr=stderr)

    def test_console_out(self):
        args = [
            "superuser",
            "superuser",
            "--no-color",
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

        # Not testing edit page messages as the id's aren't guaranteed
        # The important test is the response error and draft page messages are found
        # For good measure we'll include a test for the first and almost last lines of the output
        expected = [
            "Checking the admin and frontend responses of 4 page types ...",
            "==============================================================",
            "1. HomePage",
            "2. StandardPageOne",
            "3. StandardPageThree",
            "4. StandardPageTwo",
            "Home Page ( HomePage ) ↓",
            f"{self.live_server_url}/admin/pages/3/edit/ ← 200",
            "http://localhost:8000/ ← 200",
            "Standard Page One ( StandardPageOne ) ↓",
            f"{self.live_server_url}/admin/pages/4/edit/ ← 200",
            "http://localhost:8000/standard-page-one/ ← 200",
            "Standard Page Two ( StandardPageTwo ) ↓",
            f"{self.live_server_url}/admin/pages/5/edit/ ← 200",
            "http://localhost:8000/standard-page-two/ ← 404 probably a draft page",
            "Standard Page Three ( StandardPageThree ) ↓",
            f"{self.live_server_url}/admin/pages/6/edit/ ← 200",
            "http://localhost:8000/standard-page-three/ ← 500",
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

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)
