from rest_framework import serializers
from favourite_manager.models import FavouriteUrl, FavouriteCategory, FavouriteTag


class FavouriteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCategory
        fields = "__all__"


class FavouriteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTag
        fields = "__all__"


class FavouriteUrlSerializer(serializers.ModelSerializer):
    tags = FavouriteTagSerializer(many=True)
    category = FavouriteCategorySerializer()

    class Meta:
        model = FavouriteUrl
        fields = [
            "id",
            "user",
            "url",
            "title",
            "tags",
            "category",
            "created_at",
            "updated_at",
        ]
