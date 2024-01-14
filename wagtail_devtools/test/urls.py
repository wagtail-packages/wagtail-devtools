from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtail_devtools.api.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("wagtail-devtools-api/", include(api_urlpatterns)),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:  # pragma: no cover
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = urlpatterns + [
#     # For anything not caught by a more specific rule above, hand over to
#     # Wagtail's page serving mechanism. This should be the last pattern in
#     # the list:
#     # Alternatively, if you want Wagtail pages to be served from a subpath
#     # of your site, rather than the site root:
#     #    path("pages/", include(wagtail_urls)),
# ]
