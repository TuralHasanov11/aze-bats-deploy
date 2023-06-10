from base import models
from django.contrib import admin


class AuthorAttributesInlineAdmin(admin.StackedInline):
    model = models.AuthorAttributes


@admin.register(models.Author)
class AuthorModel(admin.ModelAdmin):
    inlines = (AuthorAttributesInlineAdmin,)


@admin.register(models.Article)
class ArticleModel(admin.ModelAdmin):
    pass


@admin.register(models.SiteInfo)
class SiteInfoModel(admin.ModelAdmin):
    pass


@admin.register(models.SiteText)
class SiteTextModel(admin.ModelAdmin):
    pass