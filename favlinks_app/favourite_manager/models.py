from django.db import models
from django.utils.translation import gettext_lazy as _

from user_manager.models import User


class FavouriteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_("Category Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Favourite Category")
        verbose_name_plural = _("Favourite Categories")
        unique_together = ("user", "name")


class FavouriteTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_("Tag Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Favourite Tag")
        verbose_name_plural = _("Favourite Tags")
        unique_together = ("user", "name")


class FavouriteUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(_("Title"), max_length=255)
    tags = models.ManyToManyField(FavouriteTag, blank=True)
    categories = models.ManyToManyField(FavouriteCategory, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        tags_to_save = kwargs.pop("tags", None)
        categories_to_save = kwargs.pop("categories", None)
        user = kwargs.pop("user", self.user)

        if tags_to_save:
            for tag in tags_to_save:
                if not user.tags.exists() or (
                    user.tags.exists() and tag not in user.tags
                ):
                    raise ValueError("Tag must belong to the same user.")
        if categories_to_save:
            for category in categories_to_save:
                if not user.categories.exists() or (
                    user.categories.exists() and category not in user.categories
                ):
                    raise ValueError("Category must belong to the same user.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Favourite Url")
        verbose_name_plural = _("Favourite Urls")
        unique_together = ("user", "url")
