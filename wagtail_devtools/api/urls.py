from django.urls import path

from .views import (  # api_view,; wagtail_core_apps,; wagtail_core_listing_pages,
    responses_api_view,
)


urlpatterns = [
    path("", responses_api_view, name="responses_api_view"),
    # path("listing-types/", wagtail_core_listing_pages, name="listing-types"),
    # path("wagtail-core-apps/", wagtail_core_apps, name="wagtail-core-apps"),
]
