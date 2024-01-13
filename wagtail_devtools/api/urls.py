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
    path("", api_view, name="api_index"),
    path("edit-types/", wagtail_core_edit_pages, name="edit-types"),
    path("form-types/", form_types, name="form-types"),
    path("listing-types/", wagtail_core_listing_pages, name="listing-types"),
    path("modeladmin-types/", model_admin_types, name="modeladmin-types"),
    path("page-types/", page_model_types, name="page-types"),
    path("settings-types/", settings_types, name="settings-types"),
    path("snippet-types/", snippet_types, name="snippet-types"),
]
