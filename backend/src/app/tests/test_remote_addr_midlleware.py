import pytest

from app.testing.drf_client import ApiClient


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def api(user):
    return ApiClient(user=user, HTTP_X_FORWARDED_FOR="100.200.250.150, 10.0.0.1")


def test_remote_addr(api):
    result = api.get("/api/v1/users/me/")

    assert result["remoteAddr"] == "100.200.250.150"
