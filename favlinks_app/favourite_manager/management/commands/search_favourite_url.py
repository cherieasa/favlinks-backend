from django.core.management.base import BaseCommand
from favourite_manager.models import FavouriteUrl


class Command(BaseCommand):
    help = "Lookup url and/or title for favourite URLs"

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, help="URL to search for")
        parser.add_argument("--title", type=str, help="Title to search for")

    def handle(self, *args, **options):
        url = options.get("url", "")
        title = options.get("title", "")

        query = FavouriteUrl.objects.filter()
        if url:
            query = query.filter(url__icontains=url)
        if title:
            query = query.filter(title__icontains=title)

        if query.exists():
            for result in query:
                self.stdout.write(
                    "- URL: {}, Title: {}".format(result.url, result.title)
                )

        self.stdout.write(f"Total results: {query.count()}")
