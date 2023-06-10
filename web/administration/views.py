from activities.models import Project, SiteVisit
from administration.forms import (ArticleForm, AuthorAttributesFormset,
                                  AuthorForm, BatSpeciesForm, ProjectForm,
                                  ProjectImageFormset, SiteVisitForm,
                                  SiteVisitImageFormset,
                                  SpeciesAttributesFormset,
                                  SpeciesImageFormset, SpeciesRedBookFormset,
                                  UserLoginForm)
from base.models import Article, Author, AuthorAttributes
from bats.models import Species
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class LoginView(auth_views.LoginView):
    authentication_form = UserLoginForm
    redirect_field_name = reverse_lazy("administration:index")
    redirect_authenticated_user = True
    template_name = "administration/auth/login.html"


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy("main:index")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "administration/dashboard.html"


class BatListView(LoginRequiredMixin, ListView):
    model = Species
    login_url = reverse_lazy("administration:index")
    template_name = "administration/services/index.html"
    context_object_name = "bats"

    def get_queryset(self):
        return super().get_queryset().select_related("genus")


@login_required
@require_http_methods(["GET", "POST"])
def batCreate(request):
    if request.POST:
        form = BatSpeciesForm(request.POST, request.FILES)
        attributes_formset = SpeciesAttributesFormset(
            data=request.POST, files=request.FILES
        )
        red_book_formset = SpeciesRedBookFormset(data=request.POST, files=request.FILES)
        images_formset = SpeciesImageFormset(data=request.POST, files=request.FILES)
        if (
            form.is_valid()
            and attributes_formset.is_valid()
            and images_formset.is_valid()
            and red_book_formset.is_valid()
        ):
            try:
                with transaction.atomic():
                    bat = form.save()
                    for attr in attributes_formset:
                        attr = attr.save(commit=False)
                        attr.species = bat
                        attr.save()
                    for img in images_formset:
                        img = img.save(commit=False)
                        img.species = bat
                        img.save()
                    for item in red_book_formset:
                        item = item.save(commit=False)
                        item.species = bat
                        item.save()
            except IntegrityError:
                messages.error(request, f'{_("Bat cannot be added!")}')
            messages.success(request, f'{_("Bat added!")}')
            return redirect("administration:bat-list")
        messages.error(request, f'{_("Bat cannot be added!")}')
    else:
        form = BatSpeciesForm()
        attributes_formset = SpeciesAttributesFormset()
        images_formset = SpeciesImageFormset()
        red_book_formset = SpeciesRedBookFormset()
    return render(
        request,
        "administration/bats/create.html",
        {
            "form": form,
            "attributes_formset": attributes_formset,
            "images_formset": images_formset,
            "red_book_formset": red_book_formset,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def batUpdate(request, id: int):
    bat = Species.objects.prefetch_related("species_images").get(id=id)
    if request.POST:
        form = BatSpeciesForm(instance=bat, data=request.POST, files=request.FILES)
        attributes_formset = SpeciesAttributesFormset(
            instance=bat, data=request.POST, files=request.FILES
        )
        images_formset = SpeciesImageFormset(
            instance=bat, data=request.POST, files=request.FILES
        )
        red_book_formset = SpeciesRedBookFormset(
            instance=bat, data=request.POST, files=request.FILES
        )
        if (
            form.is_valid()
            and attributes_formset.is_valid()
            and images_formset.is_valid()
            and red_book_formset.is_valid()
        ):
            try:
                with transaction.atomic():
                    bat = form.save()
                    attributes_formset.save()
                    images_formset.save()
                    red_book_formset.save()
            except IntegrityError:
                messages.error(request, f'{_("Bat cannot be updated!")}')
            messages.success(request, f'{_("Bat updated!")}')
            return redirect("administration:bat-update", id=id)
        messages.error(request, f'{_("Bat cannot be added!")}')
    else:
        form = BatSpeciesForm(instance=bat)
        attributes_formset = SpeciesAttributesFormset(instance=bat)
        images_formset = SpeciesImageFormset(instance=bat)
        red_book_formset = SpeciesRedBookFormset(instance=bat)
    return render(
        request,
        "administration/bats/update.html",
        {
            "form": form,
            "bat": bat,
            "attributes_formset": attributes_formset,
            "images_formset": images_formset,
            "red_book_formset": red_book_formset,
        },
    )


class BatDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Species
    login_url = reverse_lazy("administration:index")
    success_message = _("Bat deleted!")
    success_url = reverse_lazy("administration:bat-list")


@login_required
@require_http_methods(["GET", "POST"])
def authorListCreate(request):
    if request.POST:
        form = AuthorForm(data=request.POST, files=request.FILES)
        attributes_formset = AuthorAttributesFormset(
            data=request.POST, files=request.FILES
        )
        if form.is_valid() and attributes_formset.is_valid():
            try:
                with transaction.atomic():
                    author = form.save()
                    for attr in attributes_formset:
                        attr = attr.save(commit=False)
                        attr.author = author
                        attr.save()
            except IntegrityError:
                messages.error(request, f"{_('Author cannot be added!')}")
            messages.success(request, f'{_("Author added!")}')
            return redirect("administration:author-list-create")
        messages.error(request, f"{_('Author cannot be added!')}")
    else:
        form = AuthorForm()
        attributes_formset = AuthorAttributesFormset()
    authors = Author.objects.prefetch_related("author_attributes").all()
    return render(
        request,
        "administration/authors/list.html",
        {"form": form, "authors": authors, "attributes_formset": attributes_formset},
    )


@login_required
@require_http_methods(["GET", "POST", "DELETE"])
def authorUpdate(request, id):
    author = Author.objects.prefetch_related(
        Prefetch(
            "author_attributes",
            queryset=AuthorAttributes.objects.filter(
                language=translation.get_language()
            ),
        )
    ).get(id=id)
    author.author_attributes_result = author.author_attributes.all().first()
    if request.POST:
        form = AuthorForm(instance=author, data=request.POST, files=request.FILES)
        attributes_formset = AuthorAttributesFormset(
            data=request.POST, files=request.FILES
        )
        if form.is_valid() and attributes_formset.is_valid():
            try:
                with transaction.atomic():
                    author = form.save()
                    attributes_formset.save()
            except IntegrityError:
                messages.error(request, f"{_('Author cannot be updated!')}")
            messages.success(request, f'{_("Author updated!")}')
            return redirect("administration:author-update-delete", id=id)
        messages.error(request, f"{_('Author cannot be updated!')}")
    else:
        form = AuthorForm(instance=author)
        attributes_formset = AuthorAttributesFormset(instance=author)
    return render(
        request,
        "administration/authors/update.html",
        {"form": form, "author": author, "attributes_formset": attributes_formset},
    )


class AuthorDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Author
    login_url = reverse_lazy("administration:index")
    success_message = _("Author deleted!")
    success_url = reverse_lazy("administration:author-list-create")


class ArticleListCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleForm
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/articles/list.html'
    success_message = _("Article added!")
    success_url = reverse_lazy("administration:article-list-create")
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = Paginator(self.get_queryset(), self.paginate_by)
        pageNumber = self.request.GET.get('page')
        articles = pagination.get_page(pageNumber)
        context['articles'] = articles
        return context
    

class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    login_url = reverse_lazy('administration:index')
    template_name = 'administration/articles/update.html'
    context_object_name = 'article'
    success_message = _("Article was updated!")

    def get_success_url(self):
        return reverse("administration:article-update-delete", kwargs={"pk": self.object.pk})
    

class ArticleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Article
    login_url = reverse_lazy("administration:index")
    success_message = _("Article deleted!")
    success_url = reverse_lazy("administration:article-list-create")


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    login_url = reverse_lazy("administration:index")
    template_name = "administration/projects/list.html"
    context_object_name = "projects"
    paginate_by = 20


@login_required
@require_http_methods(["GET", "POST"])
def projectCreate(request):
    if request.POST:
        form = ProjectForm(data=request.POST, files=request.FILES)
        images_formset = ProjectImageFormset(data=request.POST, files=request.FILES)
        if (
            form.is_valid()
            and images_formset.is_valid()
        ):
            try:
                with transaction.atomic():
                    project = form.save()
                    for img in images_formset:
                        img.save(commit=False)
                        img.project = project
                        img.save()
            except IntegrityError:
                messages.error(request, f'{_("Project cannot be added!")}')
            messages.success(request, f'{_("Project added!")}')
            return redirect("administration:project-list")
        messages.error(request, f'{_("Project cannot be added!")}')
    else:
        form = ProjectForm()
        images_formset = ProjectImageFormset()
    return render(
        request,
        "administration/projects/create.html",
        {
            "form": form,
            "images_formset": images_formset,
        },
    )


@login_required
@require_http_methods(["GET", "POST", "DELETE"])
def projectUpdate(request, id):
    project = Project.objects.get(id=id)
    if request.POST:
        form = ProjectForm(
            instance=project, data=request.POST, files=request.FILES
        )
        images_formset = ProjectImageFormset(
            instance=project, data=request.POST, files=request.FILES
        )
        if (
            form.is_valid()
            and images_formset.is_valid()
        ):
            try:
                with transaction.atomic():
                    project = form.save()
                    images_formset.save()
            except IntegrityError:
                messages.error(request, f'{_("Project cannot be updated!")}')
            messages.success(request, f'{_("Project updated!")}')
            return redirect("administration:project-update-delete", id=id)
        messages.error(request, f'{_("Project cannot be updated!")}')
    else:
        form = ProjectForm(instance=project)
        images_formset = ProjectImageFormset(instance=project)
    return render(
        request,
        "administration/projects/update.html",
        {
            "form": form,
            "images_formset": images_formset,
        },
    )

class ProjectDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Project
    login_url = reverse_lazy("administration:index")
    success_message = _("Project deleted!")
    success_url = reverse_lazy("administration:project-list")


class SiteVisitListView(LoginRequiredMixin, ListView):
    model = SiteVisit
    login_url = reverse_lazy("administration:index")
    template_name = "administration/visits/list.html"
    context_object_name = "visits"
    paginate_by = 20


@login_required
@require_http_methods(["GET", "POST"])
def siteVisitCreate(request):
    if request.POST:
        form = SiteVisitForm(data=request.POST, files=request.FILES)
        images_formset = SiteVisitImageFormset(data=request.POST, files=request.FILES)
        if (
            form.is_valid()
            and images_formset.is_valid()
        ):
            try:
                with transaction.atomic():
                    visit = form.save()
                    for img in images_formset:
                        img = img.save(commit=False)
                        img.site_visit = visit
                        img.save()
            except IntegrityError:
                messages.error(request, f'{_("Site Visit cannot be added!")}')
            messages.success(request, f'{_("Site Visit added!")}')
            return redirect("administration:visit-list")
        messages.error(request, f'{_("Site Visit cannot be added!")}')
    else:
        form = SiteVisitForm()
        images_formset = SiteVisitImageFormset()
    return render(
        request,
        "administration/visits/create.html",
        {
            "form": form,
            "images_formset": images_formset,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def siteVisitUpdate(request, id):
    visit = SiteVisit.objects.prefetch_related("site_visit_images").get(id=id)
    if request.POST:
        form = SiteVisitForm(
            instance=visit, data=request.POST, files=request.FILES
        )
        images_formset = SiteVisitImageFormset(
            instance=visit, data=request.POST, files=request.FILES
        )
        if (
            form.is_valid()
            and images_formset.is_valid()
        ):
            try:
                with transaction.atomic():
                    visit = form.save()
                    images_formset.save()
            except IntegrityError:
                messages.error(request, f'{_("Site Visit cannot be updated!")}')
            messages.success(request, f'{_("Site Visit updated!")}')
            return redirect("administration:visit-update-delete", id=id)
        messages.error(request, f'{_("Site Visit cannot be updated!")}')
    else:
        form = SiteVisitForm(instance=visit)
        images_formset = SiteVisitImageFormset(instance=visit)
    return render(
        request,
        "administration/visits/update.html",
        {
            "form": form,
            "visit": visit,
            "images_formset": images_formset,
        },
    )

class SiteVisitDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SiteVisit
    login_url = reverse_lazy("administration:index")
    success_message = _("Site Visit deleted!")
    success_url = reverse_lazy("administration:visit-list")