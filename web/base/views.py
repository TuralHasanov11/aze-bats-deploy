from activities.models import Project, SiteVisit
from base.models import Article, Author, AuthorAttributes, SiteText
from bats.models import Species
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView


@require_GET
def index(request):
    authors = Author.objects.prefetch_related(Prefetch(
        'author_attributes', queryset=AuthorAttributes.objects.filter(language=get_language()))).all()
    for author in authors:
        author.author_attributes_result = author.author_attributes.all().first()

    bats = Species.objects.all()[:12]
    batCount = Species.objects.count()
    projectCount = Project.objects.count()
    visits = SiteVisit.objects.all()[:4]
    projects = Project.objects.all()[:4]
    visitCount = Species.objects.count()
    bannerText = SiteText.objects.filter(language=get_language()).first()

    return render(request, "base/index.html", {
        "authors": authors,
        "bats": bats,
        "projects": projects,
        "visits": visits,
        "banner": bannerText,
        "statistics": {
            "bat_count": batCount,
            "project_count": projectCount,
            "visit_count": visitCount,
        }
    })


class ArticleListView(ListView):
    model = Article
    template_name = "base/articles.html"
    paginate_by = 10
    context_object_name = "articles"


@require_GET
def search(request):
    query = request.GET.get('search', None)
    if query:
        projects = Project.objects.filter(name__contains=query)[:20]
        visits = SiteVisit.objects.filter(name__contains=query)[:20]
        bats = Species.objects.filter(name__contains=query)[:20]
        return render(request, "base/search.html", {"visits": projects, "projects": visits, "bats": bats})
    return redirect('base:index')
