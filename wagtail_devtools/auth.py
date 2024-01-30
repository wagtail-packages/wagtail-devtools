import requests


class LoginHandler:
    def __init__(self, url):
        self.url = url
        self._is_authenticated = False
        self.login_url = f"{self.url}/admin/login/"
        self.session = requests.Session()

    def login(self, username, password):
        login_form = self.session.get(self.login_url)
        if login_form.status_code == 404:
            raise Exception("Login page not found")

        user = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": login_form.cookies["csrftoken"],
        }
        response = self.session.post(self.login_url, data=user)
        if response.status_code == 200:
            self._is_authenticated = True
        return self

    def logout(self):
        self._is_authenticated = False
        self.session = requests.Session()
        return self

    def get_response(self, url):
        # a request that can be used to make authenticated requests
        # for accessing the wagtail admin pages
        response = self.session.get(url)
        return response

    def is_authenticated(self):
        return self._is_authenticated
