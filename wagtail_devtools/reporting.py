from dataclasses import dataclass, field

import requests


@dataclass
class Item:
    session: requests.Session
    app_name: str
    class_name: str
    title: str
    editor_url: str = None
    url: str = None
    url_status_code: int = None
    editor_url_status_code: int = None

    def __post_init__(self):
        self._process_url()
        self._process_editor_url()

    def _process_url(self):
        # fix the url if it doesn't start with http://localhost:8000
        if self.url:
            if not self.url.startswith("http://"):
                self.url = "http://localhost:8000" + self.url
            self.url_status_code = self.session.get_response(self.url).status_code

    def _process_editor_url(self):
        if self.editor_url:
            self.editor_url_status_code = self.session.get_response(
                self.editor_url
            ).status_code


@dataclass
class Report:
    title: str
    results: list
    session: requests.Session
    items: list = field(default_factory=list)

    def __post_init__(self):
        self.results = self._process_results()

    def _process_results(self):
        for result in self.results:
            item = Item(self.session, **result)
            self.items.append(item)

    def get_errors_500(self):
        error_500 = []
        for item in self.items:
            if item.url_status_code == 500:
                error_500.append(item)
            if item.editor_url_status_code == 500:
                error_500.append(item)
        return error_500

    def get_errors_404(self):
        error_404 = []
        for item in self.items:
            if item.url_status_code == 404:
                error_404.append(item)
            if item.editor_url_status_code == 404:
                error_404.append(item)
        return error_404

    def get_errors_302(self):
        error_302 = []
        for item in self.items:
            if item.url_status_code == 302:
                error_302.append(item)
            if item.editor_url_status_code == 302:
                error_302.append(item)
        return error_302

    def get_success_200(self):
        success = []
        for item in self.items:
            if item.url_status_code == 200:
                success.append(item)
            if item.editor_url_status_code == 200:
                success.append(item)
        return success
