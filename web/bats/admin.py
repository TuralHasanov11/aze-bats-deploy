from bats import models
from django.contrib import admin


class BatImageInlineAdmin(admin.StackedInline):
    model= models.BatImage

class BatAttributesInlineAdmin(admin.StackedInline):
    model= models.BatAttributes


class BatImageInlineAdmin(admin.StackedInline):
    model= models.BatImage


class BatRedBookInlineAdmin(admin.StackedInline):
    model= models.BatRedBook


@admin.register(models.Bat)
class BatAdmin(admin.ModelAdmin):
    list_display = ("name", "is_red_book", 'genus', 'created_at')
    prepopulated_fields = {"slug": ("name",)}  
    inlines= [BatImageInlineAdmin, BatAttributesInlineAdmin, BatRedBookInlineAdmin]


@admin.register(models.Genus)
class GenusModel(admin.ModelAdmin):
    list_display = ("name", "family")
    prepopulated_fields = {"slug": ("name",)}  

@admin.register(models.Family)
class FamilyModel(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  