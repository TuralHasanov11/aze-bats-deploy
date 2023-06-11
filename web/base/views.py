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
    authors = Author.objects.prefetch_related(Prefetch(
        'author_attributes', queryset=AuthorAttributes.objects.filter(language=get_language()))).all()

    bats = Bat.objects.all()[:12]
    batCount = Bat.objects.count()
    projectCount = Project.objects.count()
    visits = SiteVisit.objects.filter(language=get_language())[:4]
    projects = Project.objects.filter(language=get_language())[:4]
    visitCount = SiteVisit.objects.filter(language=get_language()).count()
    banner = SiteText.objects.filter(language=get_language()).only('banner_text', 'banner_title').first()
    siteInfo = SiteInfo.objects.only('banner_image', 'map_image').first()

    return render(request, "base/index.html", {
        "authors": authors,
        "bats": bats,
        "projects": projects,
        "visits": visits,
        "banner": banner,
        "banner_image": siteInfo.banner_image,
        "map": siteInfo.map_image,
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

    def get_queryset(self):
        return super().get_queryset().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article_promo_image"] = SiteInfo.objects.only('article_promo_image').first().article_promo_image
        return context
    

@require_GET
def search(request):
    query = request.GET.get('search', None)
    if query:
        projects = Project.objects.filter(name__icontains=query)[:20]
        visits = SiteVisit.objects.filter(name__icontains=query)[:20]
        bats = Bat.objects.filter(name__icontains=query)[:20]
        return render(request, "base/search.html", {"visits": visits, "projects": projects, "bats": bats})
    return redirect('base:index')


@require_GET
def about(request):
    aboutText = SiteText.objects.only("about").get(language=get_language()).about
    aboutPromoImage = SiteInfo.objects.only("about_promo_image").first().about_promo_image
    return render(request, "base/about.html", {"about_text": aboutText, 
                                               "about_promo_image": aboutPromoImage})


@require_GET
def privacyPolicy(request):
    privacyPolicyText = SiteText.objects.only("about").get(language=get_language()).privacy_policy
    privacyPolicyPromoImage = SiteInfo.objects.only("privacy_policy_promo_image").first().privacy_policy_promo_image
    return render(request, "base/privacy_policy.html", {"privacy_policy_text": privacyPolicyText, 
                                                        "privacy_policy_promo_image": privacyPolicyPromoImage})
