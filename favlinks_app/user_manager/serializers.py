from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers

from user_manager.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "confirm_password",
        )
        read_only_fields = [
            "id",
        ]

    @staticmethod
    def validate_username(value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value.lower()

    def validate(self, data):
        password_validation.validate_password(data.get("password"), self.instance)
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError(
                {"non_field_errors": ["Please enter a password and confirm it."]}
            )

        if data.get("password") != data.pop("confirm_password"):
            raise serializers.ValidationError(
                {"non_field_errors": ["Passwords do not match."]}
            )

        return data

    def create(self, validated_data):
        instance = User.objects.create(
            username=validated_data.get("username"),
            password=validated_data.get("password"),
        )
        return instance


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
        read_only_fields = [
            "id",
        ]

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Incorrect Password")
        else:
            raise serializers.ValidationError("Provide both username and password")

        return data

    def authenticate_details(self):
        return authenticate(
            username=self.validated_data["username"],
            password=self.validated_data["password"],
        )
