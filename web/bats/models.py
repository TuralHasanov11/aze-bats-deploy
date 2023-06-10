from administration import custom_models
from core import helpers
from django import urls
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Family(models.Model):
    name = custom_models.NameField(unique=True)
    slug = custom_models.SlugField()

    class Meta:
        verbose_name_plural = _("Families")

    def __str__(self):
        return self.name


class Genus(models.Model):
    name = custom_models.NameField(unique=True)
    slug = custom_models.SlugField()
    family = models.ForeignKey(Family, related_name="family", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Genus")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = helpers.generateSlug(self.name)
        return super().save(*args, **kwargs)


class Species(models.Model):
    name = custom_models.NameField(unique=True)
    slug = custom_models.SlugField()
    cover_image = custom_models.ImageField()
    genus = models.ForeignKey(Genus, related_name="genus", on_delete=models.CASCADE)
    is_red_book = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("Species")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return urls.reverse("bats:detail", kwargs={"slug": self.slug})
    
    @property
    def get_absolute_cover_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.cover_image.url)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = helpers.generateSlug(self.name)
        return super().save(*args, **kwargs)


class SpeciesAttributes(models.Model):
    species = models.ForeignKey(Species, related_name="species_attributes", on_delete=models.CASCADE)
    description = custom_models.RichTextEditorField()
    habitat = custom_models.RichTextEditorField()
    threats = custom_models.RichTextEditorField()
    distribution = custom_models.RichTextEditorField()
    conservation = custom_models.RichTextEditorField()
    biology = custom_models.RichTextEditorField()
    language = custom_models.LanguageField()

    def __str__(self):
        return str(self.species)


class SpeciesImage(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="species_images")
    image = custom_models.ImageField()

    def __str__(self):
        return str(self.species)
    

class SpeciesRedBook(models.Model):
    language = custom_models.LanguageField()
    species = models.ForeignKey(Species, related_name="species_red_book", on_delete=models.CASCADE)
    description = custom_models.RichTextEditorField()

    def __str__(self):
        return str(self.species)    