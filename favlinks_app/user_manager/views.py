from django.contrib.auth.models import update_last_login
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from user_manager.serializers import RegisterSerializer, LoginSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["POST"], detail=False, serializer_class=RegisterSerializer)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False, serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.authenticate_details()
        if not user:
            return Response(
                {"non_field_errors": [("Authentication details incorrect.")]},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, _ = Token.objects.get_or_create(user=user)
        data = self.get_serializer(user).data
        data.update({"token": token.key, "username": request.data["username"]})
        update_last_login(None, user)
        return Response(data, status=status.HTTP_200_OK)
