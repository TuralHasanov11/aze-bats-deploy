from activities import views
from django.urls import path

app_name='activities'

urlpatterns = [
    path('projects', views.ProjectListView.as_view(), name="project-list"),
    path('projects/<str:slug>', views.projectDetail, name="project-detail"),
    path('site-visits', views.SiteVisitListView.as_view(), name="site-visit-list"),
    path('site-visits/<str:slug>', views.siteVisitDetail, name="site-visit-detail"),
]
