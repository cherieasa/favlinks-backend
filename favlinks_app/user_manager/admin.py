from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from user_manager.models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ("tags", "categories")
    fieldsets = UserAdmin.fieldsets + (
        (
            _("Favourites"),
            {
                "fields": ("tags", "categories"),
            },
        ),
    )

    def tags(self, obj):
        tag_names = ", ".join(obj.tags.values_list("name", flat=True))
        if tag_names:
            return tag_names
        else:
            return "None"

    tags.short_description = _("Tags")

    def categories(self, obj):
        category_names = ", ".join(obj.categories.values_list("name", flat=True))

        if category_names:
            return category_names
        else:
            return "None"

    categories.short_description = _("categories")


admin.site.register(User, CustomUserAdmin)
