import requests
from bs4 import BeautifulSoup
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourite_manager.filters import FavouriteUrlFilter
from favourite_manager.models import (
    FavouriteCategory,
    FavouriteTag,
    FavouriteUrl,
    ValidUrl,
)
from favourite_manager.serializers import (
    FavouriteCategorySerializer,
    FavouriteTagSerializer,
    FavouriteUrlSerializer,
    FavouriteUrlCreateUpdateSerializer,
)


class ValidUrlViewSet(viewsets.GenericViewSet):
    def create(self, request):
        url = request.data.get("url", None)
        title = None
        if not url:
            return Response(
                {"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.string if soup.title else None
                is_valid = True
            else:
                is_valid = False

            ValidUrl.objects.get_or_create(
                url=url, defaults={"is_valid": is_valid, "title": title}
            )
            return Response(
                {"is_valid": is_valid, "title": title},
                status=status.HTTP_200_OK,
            )
        except ValidUrl.DoesNotExist:
            return Response(
                {"error": "URL not found"}, status=status.HTTP_404_NOT_FOUND
            )


class FavouriteCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteCategorySerializer

    def get_queryset(self):
        return FavouriteCategory.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name", None)
        existing_category = FavouriteCategory.objects.filter(
            user=request.user, name=name
        ).exists()
        if existing_category:
            return Response(
                {"error": "Category with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavouriteTagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteTagSerializer

    def get_queryset(self):
        return FavouriteTag.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name", None)
        existing_tag = FavouriteTag.objects.filter(
            user=request.user, name=name
        ).exists()
        if existing_tag:
            return Response(
                {"error": "Tag with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavouriteUrlPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "page_size"


class FavouriteUrlViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteUrlSerializer
    pagination_class = FavouriteUrlPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = FavouriteUrlFilter

    def get_queryset(self):
        return FavouriteUrl.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        url = request.data.get("url", None)
        if not url:
            return Response(
                {"error": "Url is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        existing_url = FavouriteUrl.objects.filter(user=request.user, url=url).exists()
        if existing_url:
            return Response(
                {"error": "Favourite URL with this URL already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_url_obj, created = ValidUrl.objects.get_or_create(url=url)
        if created:
            valid_url_obj.validate_url_and_get_title()
            valid_url_obj.refresh_from_db()

        if not valid_url_obj.is_valid:
            return Response(
                {"error": "URL is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = request.data.get("title", valid_url_obj.title)
        serializer = FavouriteUrlCreateUpdateSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, title=title)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        url = request.data.get("url", None)
        title = request.data.get("title", None)

        if url:
            existing_url = FavouriteUrl.objects.filter(user=request.user, url=url)
            if existing_url.exists() and existing_url.first() != instance:
                return Response(
                    {"error": "Favourite URL with this URL already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            valid_url_obj, created = ValidUrl.objects.get_or_create(url=url)
            if created:
                valid_url_obj.validate_url_and_get_title()
                valid_url_obj.refresh_from_db()

            if not valid_url_obj.is_valid:
                return Response(
                    {"error": "URL is not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = FavouriteUrlCreateUpdateSerializer(
            instance, data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, title=title, url=url)
        return Response(serializer.data)
