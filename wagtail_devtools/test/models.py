from django.db import models  # noqa: F401
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    pass


class StandardPageOne(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class StandardPageTwo(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class StandardPageThree(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


@register_snippet
class TestSnippetOne(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test Snippet One"
        verbose_name_plural = "Test Snippets One"


@register_snippet
class TestSnippetTwo(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test Snippet Two"
        verbose_name_plural = "Test Snippets Two"


@register_snippet
class TestSnippetThree(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test Snippet Three"
        verbose_name_plural = "Test Snippets Three"


class TestModelAdminOne(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Model Admin One"
        verbose_name_plural = "Model Admins One"


class TestModelAdminTwo(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Model Admin Two"
        verbose_name_plural = "Model Admins Two"


class TestModelAdminThree(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Model Admin Three"
        verbose_name_plural = "Model Admins Three"


@register_setting
class GenericSettingOne(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class GenericSettingTwo(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class GenericSettingThree(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSettingOne(BaseSiteSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSettingTwo(BaseSiteSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSettingThree(BaseSiteSetting):
    name = models.CharField(max_length=255)
