from django.urls import path

from .views import api_view, wagtail_core_apps, wagtail_core_listing_pages


urlpatterns = [
    path("", api_view, name="api_index"),
    path("listing-types/", wagtail_core_listing_pages, name="listing-types"),
    path("wagtail-core-apps/", wagtail_core_apps, name="wagtail-core-apps"),
]
