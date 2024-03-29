from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from .models import FavouriteUrl


@receiver(m2m_changed, sender=FavouriteUrl.tags.through)
def check_tags_belong_to_user(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "pre_add" and not reverse:
        user = instance.user
        if not model.objects.filter(pk__in=pk_set, user=user).exists():
            raise ValidationError("Tag must belong to the same user.")


@receiver(pre_save, sender=FavouriteUrl)
def check_category_user(sender, instance, **kwargs):
    if instance.category and instance.user != instance.category.user:
        raise ValidationError("Category must belong to the same user.")
