from django.contrib import admin
from .models import FavouriteCategory, FavouriteTag, FavouriteUrl


class FavouriteCategoryAdminView(admin.ModelAdmin):
    list_display = ["name", "user", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]


class FavouriteTagAdminView(admin.ModelAdmin):
    list_display = ["name", "user", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]


class FavouriteUrlAdminView(admin.ModelAdmin):
    list_display = ["title", "user", "url", "category","created_at", "updated_at"]
    search_fields = ["title", "url"]
    list_filter = ["created_at", "updated_at"]
    filter_horizontal = ["tags"]


admin.site.register(FavouriteCategory, FavouriteCategoryAdminView)
admin.site.register(FavouriteTag, FavouriteTagAdminView)
admin.site.register(FavouriteUrl, FavouriteUrlAdminView)
