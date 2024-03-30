from django_filters import rest_framework as filters
from .models import FavouriteUrl


class FavouriteUrlFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    url = filters.CharFilter(lookup_expr="icontains")
    category_name = filters.CharFilter(method="filter_by_category_name")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    updated_after = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")
    updated_before = filters.DateTimeFilter(field_name="updated_at", lookup_expr="lte")

    class Meta:
        model = FavouriteUrl
        fields = [
            "title",
            "url",
            "category_name",
            "created_after",
            "created_before",
            "updated_after",
            "updated_before",
        ]

    def filter_by_category_name(self, queryset, name, value):
        return queryset.filter(category__name__icontains=value)
