from administration import custom_models
from django.db import models


class Article(models.Model):
    name = custom_models.NameField()
    url = models.URLField(blank=True, null=True)
    author = models.CharField(null=False, blank=False, max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    cover_image = custom_models.ImageField()


class AuthorAttributes(models.Model):
    author = models.ForeignKey(
        Author, related_name="author_attributes", on_delete=models.CASCADE)
    name = custom_models.NameField(unique=True)
    description = custom_models.RichTextEditorField()
    language = custom_models.LanguageField()

    def __str__(self):
        return self.name


class SiteText(models.Model):
    language = custom_models.LanguageField()
    about = models.TextField(null=True, blank=True)
    banner = custom_models.RichTextEditorField()
    privacy_policy = custom_models.RichTextEditorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site Texts"

    def __str__(self):
        return f'Site Text - {self.language}'


class SiteInfo(models.Model):
    phone = models.CharField(max_length=20,  null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    banner_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/banner.jpg")
    logo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/logo.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Site Infos"

    def __str__(self):
        return self.email
