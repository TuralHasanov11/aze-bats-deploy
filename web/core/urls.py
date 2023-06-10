from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('django-admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include("base.urls")),
    path('admin/', include("administration.urls")),
    path('bats/', include("bats.urls")),
    path('activities/', include("activities.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^languages/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)