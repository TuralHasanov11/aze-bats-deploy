from bats import views
from django.urls import path

app_name = "bats"

urlpatterns = [
    path("", views.index, name="index"),
    path("gallery", views.GalleryView.as_view(), name="gallery"),
    path("<str:slug>", views.detail, name="detail"),
]
