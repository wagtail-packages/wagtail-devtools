# import logging
# import shutil

# from io import StringIO
# from sys import stderr

# from django.conf import settings
# from django.core.management import call_command
# from django.test import TestCase, override_settings, tag


# class TestE2ELoadFixtures(TestCase):
#     EXPECTED = [
#         "Creating superuser.",
#         "Updating home page.",
#         "Creating standard pages.",
#         "Creating form page.",
#         "Creating snippets.",
#         "Creating model admins.",
#         "Creating settings.",
#         "Creating collections.",
#         "Creating redirects.",
#         "Creating promoted searches.",
#         "Importing media files.",
#         "Creating second site.",
#         "Second site created.",
#         "Creating second site standard pages.",
#     ]

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(settings.MEDIA_ROOT)
#         super().tearDownClass()

#     def test_build_fixtures(self):
#         args = []
#         opts = {}

#         with StringIO() as out:
#             call_command("build_fixtures", *args, **opts, stdout=out, stderr=stderr)
#             # print(f"Command Output: \n{out.getvalue()}")  # Just for debugging

#             output = out.getvalue().splitlines()
#             self.assertEqual(self.EXPECTED, output)

#     def test_build_fixtures_clear(self):
#         args = []
#         opts = {
#             "clear": True,
#         }

#         with StringIO() as out:
#             call_command("build_fixtures", *args, **opts, stdout=out, stderr=stderr)
#             # print(f"Command Output: \n{out.getvalue()}")  # Just for debugging

#             EXPECTED = [
#                 "Clearing fixtures.",
#             ] + self.EXPECTED

#             output = out.getvalue().splitlines()
#             self.assertEqual(EXPECTED, output)


# @override_settings(DEBUG=True)
# class TestE2EAdminContentTypes(TestCase):
#     EXPECTED = [  # Not testing for existence of the edit links or cid value as can't be guaranteed
#         "Using this command:",
#         "Enter a C-Type ID from the list below",
#         "to view a report of all the admin edit pages of that type.",
#         "Page Models: 5",
#         "---------------------------------------------------------------------------------",
#         "Model Name                  App                         C-Type ID",
#         "---------------------------------------------------------------------------------",
#         "HomePage                    wagtail_devtools_test",
#         "StandardPageOne             wagtail_devtools_test",
#         "StandardPageTwo             wagtail_devtools_test",
#         "StandardPageThree           wagtail_devtools_test",
#         "FormPage                    wagtail_devtools_test",
#         "---------------------------------------------------------------------------------",
#         "Snippet Models: 3",
#         "---------------------------------------------------------------------------------",
#         "Model Name                  App                         C-Type ID",
#         "---------------------------------------------------------------------------------",
#         "TestSnippetOne              wagtail_devtools_test",
#         "TestSnippetThree            wagtail_devtools_test",
#         "TestSnippetTwo              wagtail_devtools_test",
#         "---------------------------------------------------------------------------------",
#         "ModelAdmin Models: 3",
#         "---------------------------------------------------------------------------------",
#         "Model Name                  App                         C-Type ID",
#         "---------------------------------------------------------------------------------",
#         "TestModelAdminOne           wagtail_devtools_test",
#         "TestModelAdminTwo           wagtail_devtools_test",
#         "TestModelAdminThree         wagtail_devtools_test",
#         "---------------------------------------------------------------------------------",
#         "Settings Models: 6",
#         "---------------------------------------------------------------------------------",
#         "Model Name                  App                         C-Type ID",
#         "---------------------------------------------------------------------------------",
#         "GenericSettingOne           wagtail_devtools_test",
#         "GenericSettingTwo           wagtail_devtools_test",
#         "GenericSettingThree         wagtail_devtools_test",
#         "SiteSettingOne              wagtail_devtools_test",
#         "SiteSettingTwo              wagtail_devtools_test",
#         "SiteSettingThree            wagtail_devtools_test",
#         "---------------------------------------------------------------------------------",
#     ]

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(settings.MEDIA_ROOT)
#         super().tearDownClass()

#     def setUp(self):
#         with StringIO() as out:
#             call_command("build_fixtures", stdout=out, stderr=stderr)

#     def test_console_out(self):
#         args = []
#         opts = {
#             "cid": 3,
#         }

#         with StringIO() as out:
#             call_command(
#                 "cmd_test_content_types", *args, **opts, stdout=out, stderr=out
#             )
#             output = out.getvalue().strip()

#             for line in self.EXPECTED:
#                 if line not in output:  # Just for debugging
#                     print(f"Missing this line: {line}")
#                 self.assertIn(line, output)


# @override_settings(DEBUG=True)
# class TestE2EAdminResponses(TestCase):
#     """
#     It's a challenge to get the expected output to match the actual output unless you get the output from
#     running the tox command. I'm not sure why this is the case.
#     But the best way to get the expected output is to run the tox command and copy the output from there.
#     Uncomment the print statement in the test_console_out method to see the output from the test. Then copy
#     the output and paste it into the EXPECTED list below. You'll need to add the "" and , to each line.
#     """

#     EXPECTED = [
#         "Checking the admin and frontend responses of 5 page types ...",
#         "==============================================================",
#         " 1. FormPage",
#         " 2. HomePage",
#         " 3. StandardPageOne",
#         " 4. StandardPageThree",
#         " 5. StandardPageTwo",
#         "",
#         "Home Page ( HomePage ) ↓",
#         "http://localhost:8000/admin/pages/3/edit/ ← 200",
#         "http://localhost:8000/ ← 200",
#         "",
#         "Standard Page One ( StandardPageOne ) ↓",
#         "http://localhost:8000/admin/pages/4/edit/ ← 200",
#         "http://localhost:8000/standard-page-one/ ← 200",
#         "",
#         "Standard Page Two ( StandardPageTwo ) ↓",
#         "http://localhost:8000/admin/pages/5/edit/ ← 200",
#         "http://localhost:8000/standard-page-two/ ← 404 probably a draft page",
#         "",
#         "Standard Page Three ( StandardPageThree ) ↓",
#         "http://localhost:8000/admin/pages/6/edit/ ← 200",
#         "http://localhost:8000/standard-page-three/ ← 500",
#         "",
#         "Test Form Page ( FormPage ) ↓",
#         "http://localhost:8000/admin/pages/7/edit/ ← 200",
#         "http://localhost:8000/test-form-page/ ← 200",
#         "",
#         "DASHBOARD page ...",
#         "===================",
#         "http://localhost:8000/admin/ ← 200",
#         "",
#         "PAGES list page ...",
#         "====================",
#         "http://localhost:8000/admin/pages/ ← 200",
#         "",
#         "SEARCH all page ...",
#         "====================",
#         "http://localhost:8000/admin/pages/search/ ← 200",
#         "",
#         "AGING PAGES list page ...",
#         "==========================",
#         "http://localhost:8000/admin/reports/aging-pages/ ← 200",
#         "",
#         "COLLECTIONS list page ...",
#         "==========================",
#         "http://localhost:8000/admin/collections/ ← 200",
#         "",
#         "COLLECTIONS EDIT page ...",
#         "==========================",
#         "http://localhost:8000/admin/collections/2/ ← 200",
#         "",
#         "DOCUMENTS list page ...",
#         "========================",
#         "http://localhost:8000/admin/documents/ ← 200",
#         "",
#         "DOCUMENTS edit page ...",
#         "========================",
#         "http://localhost:8000/admin/documents/edit/1/ ← 200",
#         "",
#         "GROUPS list page ...",
#         "=====================",
#         "http://localhost:8000/admin/groups/ ← 200",
#         "",
#         "GROUPS EDIT page ...",
#         "=====================",
#         "http://localhost:8000/admin/groups/1/ ← 200",
#         "",
#         "IMAGES list page ...",
#         "=====================",
#         "http://localhost:8000/admin/images/ ← 200",
#         "",
#         "IMAGES edit page ...",
#         "=====================",
#         "http://localhost:8000/admin/images/1/ ← 200",
#         "",
#         "LOCKED PAGES list page ...",
#         "===========================",
#         "http://localhost:8000/admin/reports/locked/ ← 200",
#         "",
#         "REDIRECTS list page ...",
#         "========================",
#         "http://localhost:8000/admin/redirects/ ← 200",
#         "",
#         "REDIRECTS edit page ...",
#         "========================",
#         "http://localhost:8000/admin/redirects/1/ ← 200",
#         "",
#         "SETTINGS edit pages ...",
#         "========================",
#         "http://localhost:8000/admin/settings/wagtail_devtools_test/genericsettingone/1/ ← 200",
#         "http://localhost:8000/admin/settings/wagtail_devtools_test/genericsettingtwo/1/ ← 200",
#         "http://localhost:8000/admin/settings/wagtail_devtools_test/genericsettingthree/1/ ← 200",
#         "http://localhost:8000/admin/settings/wagtail_devtools_test/sitesettingone/2/ ← 200",
#         "http://localhost:8000/admin/settings/wagtail_devtools_test/sitesettingtwo/2/ ← 200",
#         "http://localhost:8000/admin/settings/wagtail_devtools_test/sitesettingthree/2/ ← 200",
#         "",
#         "SITES list page ...",
#         "====================",
#         "http://localhost:8000/admin/sites/ ← 200",
#         "",
#         "SITES EDIT page ...",
#         "====================",
#         "http://localhost:8000/admin/sites/2/ ← 200",
#         "",
#         "SITE HISTORY list page ...",
#         "===========================",
#         "http://localhost:8000/admin/reports/site-history/ ← 200",
#         "",
#         "SNIPPETS list page ...",
#         "=======================",
#         "http://localhost:8000/admin/snippets/ ← 200",
#         "",
#         "SNIPPETS models edit pages ...",
#         "===============================",
#         "http://localhost:8000/admin/snippets/wagtail_devtools_test/testsnippetone/edit/1/ ← 200",
#         "http://localhost:8000/admin/snippets/wagtail_devtools_test/testsnippetthree/edit/1/ ← 200",
#         "http://localhost:8000/admin/snippets/wagtail_devtools_test/testsnippettwo/edit/1/ ← 200",
#         "",
#         "USERS list page ...",
#         "====================",
#         "http://localhost:8000/admin/users/ ← 200",
#         "",
#         "USERS EDIT page ...",
#         "====================",
#         "http://localhost:8000/admin/users/1/ ← 200",
#         "",
#         "WORKFLOWS list page ...",
#         "========================",
#         "http://localhost:8000/admin/workflows/list/ ← 200",
#         "",
#         "WORKFLOWS edit page ...",
#         "========================",
#         "http://localhost:8000/admin/workflows/edit/1/ ← 200",
#         "",
#         "WORKFLOWS TASKS list page ...",
#         "==============================",
#         "http://localhost:8000/admin/workflows/tasks/index/ ← 200",
#         "",
#         "WORKFLOWS TASK edit page ...",
#         "=============================",
#         "http://localhost:8000/admin/workflows/tasks/edit/1/ ← 200",
#         "",
#         "Model Admin One list page ...",
#         "==============================",
#         "http://localhost:8000/admin/wagtail_devtools_test/testmodeladminone/ ← 200",
#         "",
#         "Model Admin One edit page ...",
#         "==============================",
#         "http://localhost:8000/admin/wagtail_devtools_test/testmodeladminone/edit/1/ ← 200",
#         "",
#         "Model Admin Two list page ...",
#         "==============================",
#         "http://localhost:8000/admin/wagtail_devtools_test/testmodeladmintwo/ ← 200",
#         "",
#         "Model Admin Two edit page ...",
#         "==============================",
#         "http://localhost:8000/admin/wagtail_devtools_test/testmodeladmintwo/edit/1/ ← 200",
#         "",
#         "Model Admin Three list page ...",
#         "================================",
#         "http://localhost:8000/admin/wagtail_devtools_test/testmodeladminthree/ ← 200",
#         "",
#         "Model Admin Three edit page ...",
#         "================================",
#         "http://localhost:8000/admin/wagtail_devtools_test/testmodeladminthree/edit/1/ ← 200",
#     ]

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(settings.MEDIA_ROOT)
#         super().tearDownClass()

#     def setUp(self):
#         with StringIO() as out:
#             call_command("build_fixtures", stdout=out, stderr=stderr)

#     @tag("exclude-in-github-actions")
#     def test_console_out(self):
#         args = [
#             "superuser",
#             "superuser",
#             "--no-color",
#         ]
#         opts = {
#             "host": "http://localhost:8000",
#         }
#         logging.disable(logging.CRITICAL)

#         with StringIO() as out:
#             call_command(
#                 "cmd_test_admin_responses", *args, **opts, stdout=out, stderr=out
#             )
#             output = out.getvalue().splitlines()
#             # Useful for debugging
#             # for line in output:
#             #     print(line)

#         for line in self.EXPECTED:
#             # if line not in output:  # Just for debugging
#             #     print(f"Missing this line: {line}")
#             self.assertIn(line, output)
