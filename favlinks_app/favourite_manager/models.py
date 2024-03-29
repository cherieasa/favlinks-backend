from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class FavouriteCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Favourite Category")
        verbose_name_plural = _("Favourite Categories")


class FavouriteTag(models.Model):
    name = models.CharField(_("Tag Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Favourite Tag")
        verbose_name_plural = _("Favourite Tags")


class FavouriteUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(_("Title"), max_length=255)
    tags = models.ManyToManyField(FavouriteTag)
    category = models.ManyToManyField(FavouriteCategory)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Favourite Url")
        verbose_name_plural = _("Favourite Urls")
