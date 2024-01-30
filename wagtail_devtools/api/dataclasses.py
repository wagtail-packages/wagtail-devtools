from dataclasses import dataclass, field

from django.conf import settings
from django.urls import reverse

from wagtail_devtools.api.helpers import get_admin_edit_url, get_host


@dataclass
class ResultsModelItem:
    request: object
    item: object

    def __post_init__(self):
        self.title = self._title
        self.app_name = self._app_name
        self.class_name = self._class_name
        self.editor_url = self._editor_url
        self.url = self._url

    @property
    def _title(self):
        for key in default_field_identifier():
            if hasattr(self.item, key):
                return getattr(self.item, key)
        return "Title Field not found"

    @property
    def _app_name(self):
        return self.item._meta.app_label

    @property
    def _class_name(self):
        return self.item.__class__.__name__

    @property
    def _editor_url(self):
        return f"{get_admin_edit_url(self.request, self.item)}"

    @property
    def _url(self):
        return self.item.get_url() if hasattr(self.item, "get_url") else None

    def get(self):
        return {
            "title": self.title,
            "app_name": self.app_name,
            "class_name": self.class_name,
            "editor_url": self.editor_url,
            "url": self.url,
        }


@dataclass
class Results:
    items: list = field(default_factory=list)

    def is_duplicate(self, item):
        # avoid having duplicate results
        for i in self.items:
            if i.get("editor_url") == item.get("editor_url"):
                return True
        return False

    def add(self, item):
        if not self.is_duplicate(item):
            self.items.append(item)

    def get(self):
        return self.items


@dataclass
class ResultsListingItem:
    request: object
    app: dict

    def __post_init__(self):
        self.title = self.app["title"]
        self.app_name = None
        self.class_name = None
        self.url = None

    def get(self):
        return {
            "title": self.title,
            "app_name": self.app["app_name"],
            "class_name": self.class_name,
            "editor_url": f'{get_host(self.request)}{reverse(self.app["listing_name"])}',
            "url": self.url,
        }


def default_field_identifier():
    if hasattr(settings, "DEVTOOLS_FIELD_IDENTIFIER"):
        return settings.DEVTOOLS_FIELD_IDENTIFIER
    return ["title", "name", "username", "hostname"]
