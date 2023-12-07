from administration import models as custom_models
from core.managers import ModelManager, QuerySet
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteTextQuerySet(QuerySet):
    pass


class SiteTextManager(ModelManager):
    _queryset = SiteTextQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()

    def banner(self, language):
        return (
            self.get_queryset()
            .list_queryset()
            .filter(language=language)
            .only("language", "banner_title", "banner_text")
            .first()
        )

    def about(self, language):
        return getattr(
            self.get_queryset().list_queryset().filter(language=language).only("language", "about").first(),
            "about",
            "",
        )

    def privacy_policy(self, language):
        return getattr(
            self.get_queryset()
            .list_queryset()
            .filter(language=language)
            .only("language", "privacy_policy")
            .first(),
            "privacy_policy",
            "",
        )


class SiteInfoQuerySet(QuerySet):
    pass


class SiteInfoManager(ModelManager):
    _queryset = SiteInfoQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()

    def site_visit_promo_image(self):
        return getattr(
            self.get_queryset().detail_queryset().only("site_visit_promo_image").first(),
            "site_visit_promo_image",
            "",
        )

    def project_promo_image(self):
        return getattr(
            self.get_queryset().detail_queryset().only("project_promo_image").first(),
            "project_promo_image",
            "",
        )

    def about_promo_image(self):
        return getattr(
            self.get_queryset().detail_queryset().only("about_promo_image").first(),
            "about_promo_image",
            "",
        )

    def article_promo_image(self):
        return getattr(
            self.get_queryset().detail_queryset().only("article_promo_image").first(),
            "article_promo_image",
            "",
        )

    def bat_promo_image(self):
        return getattr(
            self.get_queryset().detail_queryset().only("bat_promo_image").first(),
            "bat_promo_image",
            "",
        )
    
    def privacy_policy_promo_image(self):
        return getattr(
            self.get_queryset().detail_queryset().only("privacy_policy_promo_image").first(),
            "privacy_policy_promo_image",
            "",
        )


class Article(models.Model):
    name = custom_models.NameField()
    url = models.URLField(blank=True, null=True)
    author = models.CharField(null=False, blank=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    cover_image = custom_models.ImageField(directory="authors")

    @property
    def author_attributes_result(self):
        return self.author_attributes.all().first()


class AuthorAttributes(models.Model):
    author = models.ForeignKey(Author, related_name="author_attributes", on_delete=models.CASCADE)
    name = custom_models.NameField(unique=True)
    description = custom_models.RichTextEditorField()
    language = custom_models.LanguageField()

    def __str__(self):
        return self.name


class SiteText(models.Model):
    language = custom_models.LanguageField()
    banner_title = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    banner_text = models.TextField(null=True, blank=True)
    privacy_policy = custom_models.RichTextEditorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    site_texts = SiteTextManager()

    class Meta:
        verbose_name_plural = _("Site Texts")

    def __str__(self):
        return _("Site Text") + f"- {self.language}"


class SiteInfo(models.Model):
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    banner_image = models.ImageField(upload_to="site/", null=True, blank=True, default="site/banner.jpg")
    map_image = models.ImageField(upload_to="site/", null=True, blank=True, default="site/map.jpg")
    about_promo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/about_promo.jpg"
    )
    privacy_policy_promo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/privacy_policy_promo.jpg"
    )
    article_promo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/article_promo.jpg"
    )
    bat_promo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/bat_promo.jpg"
    )
    project_promo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/project_promo.jpg"
    )
    site_visit_promo_image = models.ImageField(
        upload_to="site/", null=True, blank=True, default="site/site_visit_promo.jpg"
    )
    logo_image = models.ImageField(upload_to="site/", null=True, blank=True, default="site/logo.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    site_infos = SiteInfoManager()

    class Meta:
        verbose_name_plural = "Site Infos"

    def __str__(self):
        return self.email
