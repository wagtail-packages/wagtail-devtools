from django.urls import path, reverse
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem


if WAGTAIL_VERSION < (6, 0):
    from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
else:
    from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from wagtail_devtools.test.views import example_calendar, example_calendar_month

from .models import TestModelAdminOne, TestModelAdminThree, TestModelAdminTwo


class TestModelAdminOne(ModelAdmin):
    model = TestModelAdminOne


class TestModelAdminTwo(ModelAdmin):
    model = TestModelAdminTwo


class TestModelAdminThree(ModelAdmin):
    model = TestModelAdminThree


modeladmin_register(TestModelAdminOne)
modeladmin_register(TestModelAdminTwo)
modeladmin_register(TestModelAdminThree)


@hooks.register("register_admin_urls")
def register_calendar_url():
    return [
        path("calendar/", example_calendar, name="calendar"),
        path("calendar/month/", example_calendar_month, name="calendar-month"),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    submenu = Menu(
        items=[
            MenuItem("Calendar", reverse("calendar"), icon_name="date"),
            MenuItem("Current month", reverse("calendar-month"), icon_name="date"),
        ]
    )

    return SubmenuMenuItem("Calendar", submenu, icon_name="date")
