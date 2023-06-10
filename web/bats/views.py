from bats.models import Genus, Species, SpeciesAttributes, SpeciesRedBook
from django.core import paginator
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView


@require_GET
def index(request):
    genusSlug = request.GET.get("genus", None)
    if genusSlug:
        bats = Species.objects.filter(genus__slug=genusSlug)
    else:
        bats = Species.objects.all()

    pagination = paginator.Paginator(bats, 10)
    pageNumber = request.GET.get("page")
    bats = pagination.get_page(pageNumber)

    genus = Genus.objects.all()
    return render(request, "bats/index.html", {"bats": bats, "genus": genus})


class GalleryView(ListView):
    model = Species
    template_name = "bats/gallery.html"
    context_object_name = "bats"

    def get_queryset(self):
        return super().get_queryset().select_related("genus").all()


@require_GET
def detail(request, slug: str):
    bat = Species.objects.select_related("genus__family").prefetch_related(
            "species_images",
            Prefetch(
                "species_attributes",
                queryset=SpeciesAttributes.objects.filter(
                    language=translation.get_language()
                ),
            ),
            Prefetch(
                "species_red_book",
                queryset=SpeciesRedBook.objects.filter(
                    language=translation.get_language()
                ),
            ),
        ).get(slug=slug)

    bat.species_attributes_result = bat.species_attributes.all().first()
    bat.species_red_book_result = bat.species_red_book.all().first()
    return render(request, "bats/detail.html", {"bat": bat})
