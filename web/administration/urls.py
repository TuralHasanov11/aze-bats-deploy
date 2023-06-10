from administration import views
from django.urls import path

app_name='administration'

urlpatterns = [
    path('', views.DashboardView.as_view(), name="dashboard"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('bats', views.BatListView.as_view(), name="bat-list"),
    path('bats/create', views.batCreate, name="bat-create"),
    path('bats/<int:id>', views.batUpdate, name="bat-update"),
    path('bats/<int:id>/delete', views.BatDeleteView.as_view(), name="bat-delete"),
    path('projects', views.ProjectListView.as_view(), name="project-list"),
    path('projects/create', views.projectCreate, name="project-create"),
    path('projects/<int:id>', views.projectUpdate, name="project-update"),
    path('visits', views.SiteVisitListView.as_view(), name="visit-list"),
    path('visits/create', views.siteVisitCreate, name="visit-create"),
    path('visits/<int:id>', views.siteVisitUpdate, name="visit-update"),
    path('visits/<int:id>/delete', views.SiteVisitDeleteView.as_view(), name="visit-delete"),
    path('authors', views.authorListCreate, name="author-list-create"),
    path('authors/<int:id>', views.authorUpdate, name="author-update"),
    path('authors/<int:id>/delete', views.AuthorDeleteView.as_view(), name="author-delete"),
    path('articles', views.ArticleListCreateView.as_view(), name="article-list-create"),
    path('articles/<int:id>', views.ArticleUpdateView.as_view(), name="article-update"),
    path('articles/<int:id>/delete', views.ArticleUpdateView.as_view(), name="article-delete"),
]
