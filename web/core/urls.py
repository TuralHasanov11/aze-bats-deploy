from activities import sitemap as activities_sitemap
from bats import sitemap as bats_sitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

sitemaps = {
    "bats": bats_sitemap.BatSiteMap,
    "projects": activities_sitemap.ProjectSiteMap,
    "visits": activities_sitemap.SiteVisitSiteMap,
}


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("logs/", include("log_viewer.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

urlpatterns += i18n_patterns(
    path("", include("base.urls")),
    path("admin/", include("administration.urls")),
    path("bats/", include("bats.urls")),
    path("activities/", include("activities.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if "rosetta" in settings.INSTALLED_APPS:
        urlpatterns += [re_path(r"^languages/", include("rosetta.urls"))]
