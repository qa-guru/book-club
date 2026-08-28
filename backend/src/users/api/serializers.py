from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from users.models import User


PROFILE_WRITE_FIELDS = ["username", "first_name", "last_name", "email"]


class UserSerializer(serializers.ModelSerializer):
    remote_addr = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "remote_addr",
        ]
        read_only_fields = ["id", "remote_addr"]

    def get_remote_addr(self, obj: User) -> str:
        return self.context["request"].META["REMOTE_ADDR"]


@extend_schema_serializer(component_name="UserUpdate")
class UserUpdateSerializer(serializers.ModelSerializer):
    """PUT /users/me/ — full replacement; every profile field is required."""

    class Meta:
        model = User
        fields = PROFILE_WRITE_FIELDS
        extra_kwargs = {field: {"required": True} for field in PROFILE_WRITE_FIELDS}


@extend_schema_serializer(component_name="User")
class UserPartialUpdateSerializer(serializers.ModelSerializer):
    """PATCH /users/me/ — partial update; any subset of profile fields."""

    class Meta:
        model = User
        fields = PROFILE_WRITE_FIELDS
        extra_kwargs = {field: {"required": False} for field in PROFILE_WRITE_FIELDS}


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
