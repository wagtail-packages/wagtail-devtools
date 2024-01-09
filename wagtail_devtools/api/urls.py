from django.urls import path

from .views import (
    api_view,
    form_types,
    model_admin_types,
    page_model_types,
    settings_types,
    snippet_types,
    wagtail_core_edit_pages,
    wagtail_core_listing_pages,
)


urlpatterns = [
    path("", api_view, name="api_view"),
    path("page-types/", page_model_types, name="get_page_model_types"),
    path(
        "listing-types/",
        wagtail_core_listing_pages,
        name="get_wagtail_core_listing_pages",
    ),
    path(
        "edit-types/", wagtail_core_edit_pages, name="get_wagtail_core_edit_pages"
    ),
    path("settings-types/", settings_types, name="get_settings_types"),
    path("snippet-types/", snippet_types, name="get_snippet_types"),
    path("modeladmin-types/", model_admin_types, name="get_model_admin_types"),
    path("form-types/", form_types, name="get_form_types"),
]
