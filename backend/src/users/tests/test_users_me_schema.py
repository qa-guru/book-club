import pytest
from drf_spectacular.generators import SchemaGenerator


@pytest.fixture(scope="module")
def schema() -> dict:
    generator = SchemaGenerator(api_version="v1")  # type: ignore[no-untyped-call]
    generated = generator.get_schema(request=None, public=True)  # type: ignore[no-untyped-call]
    assert generated is not None
    return generated


def _request_schema(schema: dict, method: str) -> tuple[str, dict]:
    ref = schema["paths"]["/api/v1/users/me/"][method]["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    name = ref.rsplit("/", 1)[-1]
    return name, schema["components"]["schemas"][name]


def test_put_schema_requires_all_profile_fields(schema: dict) -> None:
    name, request_schema = _request_schema(schema, "put")
    assert name == "UserUpdate"
    assert set(request_schema["properties"]) == {"username", "firstName", "lastName", "email"}
    assert set(request_schema["required"]) == {"username", "firstName", "lastName", "email"}


def test_patch_schema_has_optional_profile_fields(schema: dict) -> None:
    name, request_schema = _request_schema(schema, "patch")
    assert name == "PatchedUser"
    assert set(request_schema["properties"]) == {"username", "firstName", "lastName", "email"}
    assert "required" not in request_schema


def test_user_response_schema_is_not_collapsed_to_club_author(schema: dict) -> None:
    user_schema = schema["components"]["schemas"]["User"]
    assert set(user_schema["properties"]) >= {"id", "username", "firstName", "lastName", "email", "remoteAddr"}
