from django.contrib import admin
from .models import FavouriteCategory, FavouriteTag, FavouriteUrl, ValidUrl


class ValidUrlAdminView(admin.ModelAdmin):
    list_display = ["url", "title", "is_valid", "updated_at"]
    search_fields = ["url", "title"]
    readonly_fields = ["url", "title", "updated_at", "is_valid"]
    list_filter = ["is_valid", "updated_at"]


class FavouriteCategoryAdminView(admin.ModelAdmin):
    list_display = ["name", "user", "created_at", "updated_at", "associated_urls_count"]
    search_fields = ["name", "user"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at", "associated_urls_count"]


class FavouriteTagAdminView(admin.ModelAdmin):
    list_display = ["name", "user", "created_at", "updated_at", "associated_urls_count"]
    search_fields = ["name", "user"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at", "associated_urls_count"]


class FavouriteUrlAdminView(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "url",
        "category",
        "created_at",
        "updated_at",
        "is_valid",
    ]
    search_fields = ["title", "url", "user", "category", "tag"]
    list_filter = ["created_at", "updated_at"]
    filter_horizontal = ["tags"]
    readonly_fields = ["is_valid", "created_at", "updated_at"]


admin.site.register(ValidUrl, ValidUrlAdminView)
admin.site.register(FavouriteCategory, FavouriteCategoryAdminView)
admin.site.register(FavouriteTag, FavouriteTagAdminView)
admin.site.register(FavouriteUrl, FavouriteUrlAdminView)
