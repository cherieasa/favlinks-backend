from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = settings.SUPER_ADMIN_USERNAME
        password = settings.SUPER_ADMIN_PASS
        if User.objects.filter(username__iexact=username).exists():
            self.stdout.write("The admin account already exists.")
        else:
            u = User.objects.create_superuser(username=username, password=password)
            u.is_active = True
            u.save()
            self.stdout.write("The admin account has been created.")
