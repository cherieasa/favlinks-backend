from collections import OrderedDict
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from favourite_manager.filters import FavouriteUrlFilter
from favourite_manager.models import FavouriteCategory, FavouriteTag, FavouriteUrl
from favourite_manager.serializers import (
    FavouriteCategorySerializer,
    FavouriteTagSerializer,
    FavouriteUrlSerializer,
)


class FavouriteCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteCategorySerializer

    def get_queryset(self):
        return FavouriteCategory.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name", None)
        if name is None:
            return Response(
                {"error": "Name field is required"}, status=status.HTTP_400_BAD_REQUEST
            )

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
        if name is None:
            return Response(
                {"error": "Name field is required"}, status=status.HTTP_400_BAD_REQUEST
            )

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
    page_size = 100
    max_page_size = 100
    page_size_query_param = "page_size"
    page_query_description = _(
        'A page number within the paginated result set. page "-1" would return a list result '
        "without paginated"
    )

    def get_paginated_response(self, data, tags):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("tags", tags),
                    ("results", data),
                ]
            )
        )


class FavouriteUrlViewSet(PageNumberPagination, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteUrlSerializer
    filter_backends = [DjangoFilterBackend, FavouriteUrlFilter]
    pagination_class = FavouriteUrlPagination

    def get_queryset(self):
        return FavouriteUrl.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
