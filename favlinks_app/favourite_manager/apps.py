from django.apps import AppConfig


class FavouriteManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "favourite_manager"
    verbose_name = "Favourite Manager"

    def ready(self):
        import favourite_manager.signals
