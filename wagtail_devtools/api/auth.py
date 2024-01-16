from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.test import RequestFactory
from requests.sessions import Session


User = get_user_model()


class AdminSession(Session):
    def __init__(self, login_url=None, username=None, password=None) -> None:
        super().__init__()
        if not hasattr(settings, "WAGTAIL_DEVTOOLS_ENABLED"):
            raise Exception("WAGTAIL_DEVTOOLS not configured in settings")
        if not hasattr(settings, "WAGTAIL_DEVTOOLS_TEST_USER"):
            self.login_url = login_url or "/admin/login/"
            self.username = username
            self.password = password
        else:
            self.login_url = settings.WAGTAIL_DEVTOOLS_TEST_USER["login_url"]
            self.username = settings.WAGTAIL_DEVTOOLS_TEST_USER["username"]
            self.password = settings.WAGTAIL_DEVTOOLS_TEST_USER["password"]

        self.user_model = get_user_model()
        self.user = None
        self.logged_in = False

    def _check_login(self) -> Session:
        authenticated_user = authenticate(
            username=self.username, password=self.password
        )
        if authenticated_user is not None:
            # A backend authenticated the credentials
            self.user = authenticated_user
            self.logged_in = True

    def get_request(self):
        # a request that can be used to make authenticated requests
        # for accessing the wagtail admin pages
        if not self.user.is_authenticated:
            self._check_login()
        request = RequestFactory().get(self.login_url)
        request.session = self.cookies
        return request
