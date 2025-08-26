import pytest


pytestmark = [pytest.mark.django_db]


def test_ok(as_anon, user_request_data):
    as_anon.post("/api/v1/users/register/", user_request_data)


def test_try_to_register_existing_user(as_anon, user_request_data):
    as_anon.post("/api/v1/users/register/", user_request_data)
    got = as_anon.post("/api/v1/users/register/", user_request_data, as_response=True)
    assert got.status_code == 400
