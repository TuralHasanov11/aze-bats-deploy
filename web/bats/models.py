from administration import models as custom_models
from core import helpers
from django.urls import reverse
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


class Bat(models.Model):
    name = custom_models.NameField(unique=True)
    slug = custom_models.SlugField()
    cover_image = custom_models.ImageField(directory="bats")
    genus = models.ForeignKey(Genus, related_name="genus", on_delete=models.CASCADE)
    is_red_book = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bats:detail", kwargs={"slug": self.slug})
    
    @property
    def get_absolute_cover_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.cover_image.url)
    
    @property
    def bat_attributes_result(self):
        return self.bat_attributes.all().first()
    
    @property
    def bat_red_book_result(self):
        return self.bat_red_book.all().first()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = helpers.generateSlug(self.name)
        return super().save(*args, **kwargs)


class BatAttributes(models.Model):
    bat = models.ForeignKey(Bat, related_name="bat_attributes", on_delete=models.CASCADE)
    description = custom_models.RichTextEditorField()
    habitat = custom_models.RichTextEditorField()
    threats = custom_models.RichTextEditorField()
    distribution = custom_models.RichTextEditorField()
    conservation = custom_models.RichTextEditorField()
    biology = custom_models.RichTextEditorField()
    language = custom_models.LanguageField()


class BatImage(models.Model):
    bat = models.ForeignKey(Bat, on_delete=models.CASCADE, related_name="bat_images")
    image = custom_models.ImageField(directory="bats")

    def __str__(self):
        return str(self.image.url)
    

class BatRedBook(models.Model):
    language = custom_models.LanguageField()
    bat = models.ForeignKey(Bat, related_name="bat_red_book", on_delete=models.CASCADE)
    description = custom_models.RichTextEditorField() 