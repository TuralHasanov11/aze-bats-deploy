from activities.models import (Project, ProjectAttributes, SiteVisit,
                               SiteVisitAttributes)
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView


class ProjectListView(ListView):
    model = Project
    template_name = "activities/projects.html"
    paginate_by = 10
    context_object_name = "projects"


@require_GET
def projectDetail(request, slug: str):
    project = Project.objects.prefetch_related(
        "project_images",
        Prefetch(
            "project_attributes",
            queryset=ProjectAttributes.objects.filter(language=get_language()),
        ),
    ).get(slug=slug)
    project.project_attributes_result = project.project_attributes.all().first()
    return render(request, "activities/project.html", {"project": project})


class SiteVisitListView(ListView):
    model = SiteVisit
    template_name = "activities/visits.html"
    paginate_by = 10
    context_object_name = "visits"


@require_GET
def siteVisitDetail(request, slug: str):
    visit = SiteVisit.objects.prefetch_related(
        "site_visit_images",
        Prefetch(
            "site_visit_attributes",
            queryset=SiteVisitAttributes.objects.filter(language=get_language()),
        ),
    ).get(slug=slug)
    visit.site_visit_attributes_result = visit.site_visit_attributes.all().first()
    return render(request, "activities/visit.html", {"visit": visit})
