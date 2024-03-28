from django.db import models
from django.utils.translation import gettext_lazy as _


class FavouriteCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FavouriteTag(models.Model):
    name = models.CharField(_("Tag Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FavouriteUrl(models.Model):
    url = models.URLField()
    title = models.CharField(_("Title"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
