import django_filters
from .models import FavouriteUrl


class FavouriteUrlFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    url = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FavouriteUrl
        fields = ["title", "url"]
