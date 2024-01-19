import os
import shutil

# from django.core.management import call_command
from django.test.runner import DiscoverRunner


# from io import StringIO


class WagtailDevToolsTestRunner(DiscoverRunner):
    """A test runner to rebuild build fixtures.

    After the test suite has run, this test runner will rebuild the test-media folder
    by running the build_fixtures command.

    The data inst't required as it uses the in test database, but the test-media folder
    needs to be reset.

    WE ARE NOT USING THIS AT THE MOMENT"""

    # def teardown_test_environment(self, **kwargs):
    #     super().teardown_test_environment(**kwargs)
    #     remove_media_root()
    #     with StringIO() as _:
    #         # Don't want to see the output of the command
    #         call_command("build_fixtures", "--clear", stdout=_)
    #     print("Restored the test-media folder")


def remove_media_root():
    media_root = os.path.join(os.getcwd(), "test-media")
    if os.path.exists(media_root):
        shutil.rmtree(media_root)
