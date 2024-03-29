from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import FavouriteUrl


@receiver(m2m_changed, sender=FavouriteUrl.tags.through)
def check_tags_belong_to_user(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "pre_add" and not reverse:
        user = instance.user
        if not model.objects.filter(pk__in=pk_set, user=user).exists():
            raise ValueError(
                "All tags must belong to the same user as the favourite URL."
            )


@receiver(m2m_changed, sender=FavouriteUrl.categories.through)
def check_categories_belong_to_user(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action == "pre_add" and not reverse:
        user = instance.user
        if not model.objects.filter(pk__in=pk_set, user=user).exists():
            raise ValueError(
                "All categories must belong to the same user as the favourite URL."
            )
