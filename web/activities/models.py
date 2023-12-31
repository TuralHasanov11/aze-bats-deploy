from administration import models as custom_models
from core import helpers
from django.db import models
from django.urls import reverse


class Project(models.Model):
    name = custom_models.NameField()
    slug = custom_models.SlugField()
    cover_image = custom_models.ImageField(directory="projects")
    description = custom_models.RichTextEditorField()
    language = custom_models.LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = helpers.generateSlug(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("bats:detail", kwargs={"slug": self.slug})


class SiteVisit(models.Model):
    name = custom_models.NameField()
    slug = custom_models.SlugField()
    cover_image = custom_models.ImageField(directory="site_visits")
    description = custom_models.RichTextEditorField()
    results = custom_models.RichTextEditorField()
    language = custom_models.LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Visit"
        verbose_name_plural = "Site Visits"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = helpers.generateSlug(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("bats:detail", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_images"
    )
    image = custom_models.ImageField(directory="projects")

    def __str__(self) -> str:
        return str(self.project)


class SiteVisitImage(models.Model):
    site_visit = models.ForeignKey(
        SiteVisit, on_delete=models.CASCADE, related_name="site_visit_images"
    )
    image = custom_models.ImageField(directory="site_visits")

    def __str__(self) -> str:
        return str(self.site_visit)
