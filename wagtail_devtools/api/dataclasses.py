from dataclasses import dataclass

from wagtail_devtools.api.helpers import get_admin_edit_url


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
        return (
            self.item.title
            if hasattr(self.item, "title")
            else self.item.name
            if hasattr(self.item, "name")
            else self.item.hostname
            if hasattr(self.item, "hostname")
            else self.item.username
            if hasattr(self.item, "username")
            else self.item.__str__()
        )

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
class ResultsListingItem:
    request: object
    page: object
    editor_url: str

    def __post_init__(self):
        self.title = self._generate_title
        self.app_name = None
        self.class_name = None
        self.url = None

    @property
    def _generate_title(self):
        splits = self.page.split("_")
        splits = " ".join(splits)
        splits = splits.split(":")
        splits = " ".join(splits)
        splits = splits.replace("wagtail", "")
        splits = splits.lower()  # just in case

        def upper_words(s):
            return " ".join(w.capitalize() for w in s.split(" "))

        return upper_words(splits)

    def get(self):
        return {
            "title": self.title,
            "app_name": self.app_name,
            "class_name": self.class_name,
            "editor_url": self.editor_url,
            "url": self.url,
        }
