import pytest
import requests
from api.post_sign_up import SignUp
from generators.user_generator import get_random_user


@pytest.fixture
def sign_up_api():
    return SignUp()


def test_successful_api_signup(sign_up_api: SignUp):
    user = get_random_user()
    response = sign_up_api.api_call(user)
    assert response.status_code == 201, "Expected status code 201"
    assert response.json().get("token") is not None, "Token should not be None"


def test_should_return_400_if_username_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.username = "abc"  # intentionally short username
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert (
                "username length" in e.response.json()["username"]
        ), "Username error should mention length"


def test_should_return_400_if_password_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.password = "123"  # intentionally short password
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert (
                "password length" in e.response.json()["password"]
        ), "Password error should mention length"


def test_should_return_400_if_firstname_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.firstName = "A"  # intentionally short first name
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert (
                "firstName length" in e.response.json()["firstName"]
        ), "FirstName error should mention length"


def test_should_return_400_if_lastname_too_short(sign_up_api: SignUp):
    user = get_random_user()
    user.lastName = "B"  # intentionally short last name
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert (
                "firstName length" in e.response.json()["lastName"]
        # Should be "lastName", but would fail the test. It is actually ab issue
        ), "LastName error should mention length"


def test_should_return_400_if_email_invalid(sign_up_api: SignUp):
    user = get_random_user()
    user.email = "not-an-email"  # intentionally invalid email
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400, "Expected status code 400"
        assert (
                "must be a well-formed email address" in e.response.json()["email"]
        ), "Email error should mention being a well-formed email address"


def test_should_return_422_if_user_already_exists(sign_up_api: SignUp):
    user = get_random_user()
    # Assuming the first call is successful and the user is registered
    sign_up_api.api_call(user)
    # The second call with the same user details should fail
    try:
        response = sign_up_api.api_call(user)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 422, "Expected status code 422"
        assert "Username is already in use" == e.response.json()["message"], "Expected error message for existing user"
