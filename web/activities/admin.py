from activities import models
from django.contrib import admin


class ProjectImageInlineAdmin(admin.StackedInline):
    model = models.ProjectImage


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInlineAdmin]
    list_display = ('name', 'language')
    prepopulated_fields = {'slug': ('name',)}


class SiteVisitImageInlineAdmin(admin.StackedInline):
    model = models.SiteVisitImage


@admin.register(models.SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    inlines = [SiteVisitImageInlineAdmin]
    list_display = ('name', 'language')
    prepopulated_fields = {'slug': ('name',)}
