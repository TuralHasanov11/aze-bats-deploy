from activities.models import Project, SiteVisit
from base.models import Article, Author, AuthorAttributes, SiteInfo, SiteText
from bats.models import Bat
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView


@require_GET
def index(request):
    authors = Author.objects.prefetch_related(
        Prefetch("author_attributes", queryset=AuthorAttributes.objects.filter(language=get_language()))
    ).all()

    bats = Bat.objects.all()[:12]
    batCount = Bat.objects.count()
    projectCount = Project.objects.count()
    visits = SiteVisit.objects.filter(language=get_language())[:4]
    projects = Project.objects.filter(language=get_language())[:4]
    visitCount = SiteVisit.objects.filter(language=get_language()).count()
    banner = SiteText.site_texts.banner(language=get_language())
    siteInfo = SiteInfo.objects.only("banner_image", "map_image").first()

    return render(
        request,
        "base/index.html",
        {
            "authors": authors,
            "bats": bats,
            "projects": projects,
            "visits": visits,
            "banner": banner,
            "banner_image": getattr(siteInfo, "banner_image", ""),
            "map": getattr(siteInfo, "map_image", ""),
            "statistics": {
                "bat_count": batCount,
                "project_count": projectCount,
                "visit_count": visitCount,
            },
        },
    )


class ArticleListView(ListView):
    model = Article
    template_name = "base/articles.html"
    paginate_by = 10
    context_object_name = "articles"

    def get_queryset(self):
        return super().get_queryset().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article_promo_image"] = SiteInfo.site_infos.article_promo_image()
        return context


@require_GET
def search(request):
    query = request.GET.get("search", None)
    if query:
        projects = Project.objects.filter(name__icontains=query)[:20]
        visits = SiteVisit.objects.filter(name__icontains=query)[:20]
        bats = Bat.objects.filter(name__icontains=query)[:20]
        return render(request, "base/search.html", {"visits": visits, "projects": projects, "bats": bats})
    return redirect("base:index")


@require_GET
def about(request):
    aboutText = SiteText.site_texts.about(language=get_language())
    about_promo_image = SiteInfo.site_infos.about_promo_image()
    return render(
        request, "base/about.html", {"about_text": aboutText, "about_promo_image": about_promo_image}
    )


@require_GET
def privacyPolicy(request):
    privacy_policy_text = SiteText.site_texts.privacy_policy(language=get_language())
    privacy_policy_promo_image = SiteInfo.site_infos.privacy_policy_promo_image()
    return render(
        request,
        "base/privacy_policy.html",
        {
            "privacy_policy_text": privacy_policy_text,
            "privacy_policy_promo_image": privacy_policy_promo_image,
        },
    )
