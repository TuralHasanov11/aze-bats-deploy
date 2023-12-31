from activities.models import Project, SiteVisit
from base.models import SiteInfo
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView


class ProjectListView(ListView):
    model = Project
    template_name = "activities/projects.html"
    paginate_by = 10
    context_object_name = "projects"

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at").filter(language=get_language())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_promo_image"] = (
            SiteInfo.site_infos.project_promo_image()
        )
        return context


@require_GET
def projectDetail(request, slug: str):
    project = Project.objects.prefetch_related("project_images").get(slug=slug)
    return render(request, "activities/project.html", {"project": project})


class SiteVisitListView(ListView):
    model = SiteVisit
    template_name = "activities/visits.html"
    paginate_by = 10
    context_object_name = "visits"

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at").filter(language=get_language())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_visit_promo_image"] = SiteInfo.site_infos.site_visit_promo_image()
        return context


@require_GET
def siteVisitDetail(request, slug: str):
    visit = SiteVisit.objects.prefetch_related("site_visit_images").get(slug=slug)
    return render(request, "activities/visit.html", {"visit": visit})
