from rest_framework import serializers
from favourite_manager.models import FavouriteUrl, FavouriteCategory, FavouriteTag


class FavouriteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCategory
        fields = ["id", "user", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        return FavouriteCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class FavouriteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTag
        fields = ["id", "user", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        return FavouriteTag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


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
