import pytest
from rest_framework.test import APIClient

from users.api.serializers import UserPartialUpdateSerializer, UserUpdateSerializer
from users.models import User


PROFILE = {
    "username": "alice",
    "first_name": "Alice",
    "last_name": "Reader",
    "email": "alice@example.com",
}


@pytest.fixture
def api_user(db: None) -> User:
    password = "pass12345"  # noqa: S105
    return User.objects.create_user(
        username="alice",
        password=password,
        first_name="Old",
        last_name="Name",
        email="old@example.com",
    )


@pytest.fixture
def api_client(api_user: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=api_user)
    return client


@pytest.mark.django_db
def test_put_serializer_requires_every_profile_field() -> None:
    serializer = UserUpdateSerializer(data={"username": "alice"})
    assert serializer.is_valid() is False
    assert set(serializer.errors) == {"first_name", "last_name", "email"}


@pytest.mark.django_db
def test_patch_serializer_accepts_a_single_field() -> None:
    serializer = UserPartialUpdateSerializer(data={"username": "alice"})
    assert serializer.is_valid() is True


def test_put_rejects_partial_body(api_client: APIClient) -> None:
    response = api_client.put("/api/v1/users/me/", {"username": "alice"}, format="json")
    assert response.status_code == 400
    assert "firstName" in response.data
    assert "lastName" in response.data
    assert "email" in response.data


def test_put_replaces_full_profile(api_client: APIClient, api_user: User) -> None:
    response = api_client.put("/api/v1/users/me/", PROFILE, format="json")
    assert response.status_code == 200
    api_user.refresh_from_db()
    assert api_user.first_name == "Alice"
    assert api_user.last_name == "Reader"
    assert api_user.email == "alice@example.com"
    assert response.data["username"] == "alice"
    assert "remoteAddr" in response.data


def test_patch_updates_selected_fields(api_client: APIClient, api_user: User) -> None:
    response = api_client.patch("/api/v1/users/me/", {"firstName": "Alice"}, format="json")
    assert response.status_code == 200
    api_user.refresh_from_db()
    assert api_user.first_name == "Alice"
    assert api_user.last_name == "Name"
    assert api_user.email == "old@example.com"
