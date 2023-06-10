from bats.models import Genus, Bat, BatAttributes, BatRedBook
from base.models import SiteInfo
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
        bats = Bat.objects.order_by('name').filter(genus__slug=genusSlug)
    else:
        bats = Bat.objects.order_by('name').all()

    pagination = paginator.Paginator(bats, 10)
    pageNumber = request.GET.get("page")
    bats = pagination.get_page(pageNumber)
    batPromoImage = SiteInfo.objects.only('bat_promo_image').first().bat_promo_image

    genus = Genus.objects.all()
    return render(request, "bats/index.html", {"bats": bats, "genus": genus, "bat_promo_image": batPromoImage})


class GalleryView(ListView):
    model = Bat
    template_name = "bats/gallery.html"
    context_object_name = "bats"

    def get_queryset(self):
        return super().get_queryset().select_related("genus").order_by('name').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bat_promo_image"] = SiteInfo.objects.only('bat_promo_image').first().bat_promo_image
        return context
    

@require_GET
def detail(request, slug: str):
    bat = Bat.objects.select_related("genus__family").prefetch_related(
            "bat_images",
            Prefetch(
                "bat_attributes",
                queryset=BatAttributes.objects.filter(
                    language=translation.get_language()
                ),
            ),
            Prefetch(
                "bat_red_book",
                queryset=BatRedBook.objects.filter(
                    language=translation.get_language()
                ),
            ),
        ).get(slug=slug)
    return render(request, "bats/detail.html", {"bat": bat})
