from django.db import models  # noqa: F401
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    pass


@register_snippet
class TestSnippet(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


if not WAGTAIL_VERSION >= (5, 2):

    class TestModelAdmin(models.Model):
        title = models.CharField(max_length=255)

        def __str__(self):
            return self.title


@register_setting
class GenericSetting(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSetting(BaseSiteSetting):
    name = models.CharField(max_length=255)
