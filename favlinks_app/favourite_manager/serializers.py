from rest_framework import serializers
from favourite_manager.models import FavouriteUrl, FavouriteCategory, FavouriteTag


class FavouriteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCategory
        fields = [
            "id",
            "user",
            "name",
            "created_at",
            "updated_at",
            "associated_urls_count",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "associated_urls_count",
        ]

    def create(self, validated_data):
        return FavouriteCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class FavouriteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTag
        fields = [
            "id",
            "user",
            "name",
            "created_at",
            "updated_at",
            "associated_urls_count",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "associated_urls_count",
        ]

    def create(self, validated_data):
        return FavouriteTag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class FavouriteUrlSerializer(serializers.ModelSerializer):
    tags = FavouriteTagSerializer(many=True, required=False)
    category = FavouriteCategorySerializer(required=False)
    title = serializers.CharField(required=False)

    class Meta:
        model = FavouriteUrl
        fields = [
            "id",
            "user",
            "url",
            "title",
            "tags",
            "category",
            "is_valid",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at", "is_valid"]

    def create(self, validated_data):
        return FavouriteUrl.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class FavouriteUrlCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=FavouriteCategory.objects.all(), required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=FavouriteTag.objects.all(), many=True, required=False
    )
    title = serializers.CharField(required=False)

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
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["user"]
        category = validated_data.pop("category", None)
        tags = validated_data.pop("tags", None)
        favourite_url = FavouriteUrl.objects.create(**validated_data)
        if category:
            category = FavouriteCategory.objects.filter(
                id=category.id, user=user
            ).first()
            if category:
                favourite_url.category = category
                favourite_url.save()

        if tags:
            tag_ids = [tag.id for tag in tags]
            tags_queryset = FavouriteTag.objects.filter(id__in=tag_ids, user=user)
            favourite_url.tags.set(tags_queryset)

        return favourite_url

    def update(self, instance, validated_data):
        user = self.context["user"]
        tags = validated_data.get("tags", None)
        category = validated_data.get("category", None)

        if category is None:
            instance.category = None
        else:
            category = FavouriteCategory.objects.filter(
                id=category.id, user=user
            ).first()
            if category:
                instance.category = category
                instance.save()

        if tags is None:
            instance.tags.clear()
        else:
            tag_ids = [tag.id for tag in tags]
            tags_queryset = FavouriteTag.objects.filter(id__in=tag_ids, user=user)
            instance.tags.set(tags_queryset)

        instance.url = validated_data.get("url", instance.url)
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        return instance
