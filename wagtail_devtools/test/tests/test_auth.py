from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from wagtail_devtools.api.auth import AdminSession


User = get_user_model()


class TestAuthSession(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            "username": "admin",
            "email": "",
            "password": "admin",
        }
        User.objects.create_superuser(**cls.data)

    @override_settings(WAGTAIL_DEVTOOLS_ENABLED=True)
    def test_check_login(self):
        session = AdminSession(
            login_url="http://localhost:8000/admin/login/",
            username=self.data["username"],
            password=self.data["password"],
        )
        session._check_login()

        self.assertTrue(session.logged_in)

    @override_settings(WAGTAIL_DEVTOOLS_ENABLED=True)
    def test_get_request(self):
        session = AdminSession(
            login_url="http://localhost:8000/admin/login/",
            username=self.data["username"],
            password=self.data["password"],
        )
        session._check_login()

        request = session.get_request()
        self.assertIsInstance(request, object)
