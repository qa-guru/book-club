from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from app.api.request import AuthenticatedRequest
from users.api.serializers import (
    UserPartialUpdateSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from users.api.services import UserRegisterService
from users.models import User


@extend_schema_view(
    get=extend_schema(responses={200: UserSerializer}),
    put=extend_schema(request=UserUpdateSerializer, responses={200: UserSerializer}),
    patch=extend_schema(request=UserPartialUpdateSerializer, responses={200: UserSerializer}),
    delete=extend_schema(responses={204: None}),
)
class SelfView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    request: AuthenticatedRequest

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == "PUT":
            return UserUpdateSerializer
        if self.request.method == "PATCH":
            return UserPartialUpdateSerializer
        return UserSerializer

    def get(self, request: AuthenticatedRequest) -> Response:
        return self._respond_user(self.get_object())

    def delete(self, request: AuthenticatedRequest) -> Response:
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: AuthenticatedRequest) -> Response:
        return self._update(partial=False)

    def patch(self, request: AuthenticatedRequest) -> Response:
        return self._update(partial=True)

    def get_object(self) -> User:
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)

    def _update(self, *, partial: bool) -> Response:
        serializer = self.get_serializer(self.get_object(), data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return self._respond_user(user)

    def _respond_user(self, user: User) -> Response:
        return Response(UserSerializer(user, context=self.get_serializer_context()).data)


class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_creator = UserRegisterService(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        user = user_creator()

        user_serializer = UserSerializer(user, context=self.get_serializer_context())
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
