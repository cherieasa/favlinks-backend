from django.core.management.base import BaseCommand
from favourite_manager.models import FavouriteUrl


class Command(BaseCommand):
    help = "Lookup url and/or title for favourite URLs"

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, help="URL to search for")
        parser.add_argument("--title", type=str, help="Title to search for")
        parser.add_argument("--category", type=str, help="Category to search for")
        parser.add_argument("--tag", type=str, help="Tag to search for")

    def handle(self, *args, **options):
        url = options.get("url", "")
        title = options.get("title", "")
        category = options.get("category", "")
        tag = options.get("tag", "")

        query = FavouriteUrl.objects.filter()
        if url:
            query = query.filter(url__icontains=url)
        if title:
            query = query.filter(title__icontains=title)
        if category:
            query = query.filter(category__name__icontains=category)
        if tag:
            query = query.filter(tags__icontains=tag)

        if query.exists():
            for result in query:
                self.stdout.write(
                    "- URL: {}, Title: {}, Category: {}, Tags: {}".format(
                        result.url,
                        result.title,
                        result.category,
                        ", ".join([tag.name for tag in result.tags.all()]),
                    )
                )

        self.stdout.write(f"Total results: {query.count()}")
