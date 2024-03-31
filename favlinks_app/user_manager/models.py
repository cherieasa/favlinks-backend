from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __str__(self):
        return self.username

    @property
    def tags(self):
        from favourite_manager.models import FavouriteTag

        return FavouriteTag.objects.filter(user=self).values_list("id", flat=True)

    @property
    def categories(self):
        from favourite_manager.models import FavouriteCategory

        return FavouriteCategory.objects.filter(user=self)
