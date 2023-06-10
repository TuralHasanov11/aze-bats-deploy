from base import views
from django.urls import path

app_name = 'base'

urlpatterns = [
    path('', views.index, name="index"),
    path('articles', views.ArticleListView.as_view(), name="articles"),
    path('search', views.search, name="search"),
]
