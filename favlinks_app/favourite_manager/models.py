from unicodedata import category
from bs4 import BeautifulSoup
import requests

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from user_manager.models import User


class FavouriteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_("Category Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def associated_urls_count(self):
        return FavouriteUrl.objects.filter(category=self).count()

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

    @property
    def associated_urls_count(self):
        return FavouriteUrl.objects.filter(tags__in=[self]).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Favourite Tag")
        verbose_name_plural = _("Favourite Tags")
        unique_together = ("user", "name")


class ValidUrl(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(_("Title"), max_length=255, blank=True, null=True)
    is_valid = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def validate_url_and_get_title(self) -> None:
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                self.title = soup.title.string if soup.title else ""
                self.is_valid = True
            else:
                self.is_valid = False
            self.save()
        except requests.RequestException:
            self.is_valid = False
            self.save()


class FavouriteUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(_("Title"), max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        FavouriteCategory, blank=True, null=True, on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(FavouriteTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        tags_to_save = kwargs.pop("tags", None)
        category_to_save = kwargs.pop("category", None)
        user = kwargs.pop("user", self.user)

        if tags_to_save:
            for tag in tags_to_save:
                if not user.tags.exists() or (
                    user.tags.exists() and tag not in user.tags
                ):
                    raise ValidationError("Tag must belong to the same user.")
        if category_to_save:
            if not user.categories.exists() or (
                user.categories.exists() and category_to_save not in user.categories
            ):
                raise ValidationError("Category must belong to the same user.")
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        valid_url = ValidUrl.objects.filter(url=self.url)
        if valid_url.exists():
            return valid_url.first().is_valid
        return False

    class Meta:
        verbose_name = _("Favourite Url")
        verbose_name_plural = _("Favourite Urls")
        unique_together = ("user", "url")
