import asyncio
from datetime import timedelta
import pytest
from app.service import auth_service
from app.dto.user import UserDTO
from jose import jwt


def test_create_access_token():
    token = auth_service.create_access_token(
        "user", 1, "admin", expires_delta=timedelta(minutes=60)
    )
    assert isinstance(token, str)
    payload = jwt.get_unverified_claims(token)
    assert payload["sub"] == "user"
    assert payload["id"] == 1
    assert payload["role"] == "admin"


def test_authenticate_user_success(monkeypatch):
    class FakeUser:
        username = "user"
        id = 1
        role = "admin"
        hashed_password = auth_service.bcrypt_context.hash("123456")

    monkeypatch.setattr(
        auth_service.user_repository, "authenticate_user", lambda u, p: FakeUser()
    )
    result = auth_service.authenticate_user("user", "123456")
    assert "access_token" in result


def test_authenticate_user_fail(monkeypatch):
    monkeypatch.setattr(
        auth_service.user_repository, "authenticate_user", lambda u, p: False
    )
    with pytest.raises(Exception):
        auth_service.authenticate_user("user", "wrong")


def test_get_current_user_valid_token(monkeypatch):
    token = auth_service.create_access_token(
        "user", 1, "admin", expires_delta=timedelta(minutes=60)
    )
    result = asyncio.run(auth_service.get_current_user(token))
    assert result["username"] == "user"
    assert result["id"] == 1
    assert result["user_role"] == "admin"


def test_get_current_user_invalid_token():
    with pytest.raises(Exception):
        asyncio.run(auth_service.get_current_user("invalid.token"))


def test_create_user(monkeypatch):
    monkeypatch.setattr(auth_service.user_repository, "create_user", lambda user: True)
    user = UserDTO(
        username="testuser",
        email="test@user.com",
        first_name="Test",
        last_name="User",
        password="123456",
        role="user",
        phone_number="123456789",
    )
    assert auth_service.create_user(user) is None


def test_get_current_user_expired_token(monkeypatch):
    token = auth_service.create_access_token(
        "user", 1, "admin", expires_delta=timedelta(minutes=-1)
    )
    with pytest.raises(Exception):
        asyncio.run(auth_service.get_current_user(token))


def test_get_current_user_missing_claims(monkeypatch):
    from jose import jwt

    token = jwt.encode({}, auth_service.SECRET_KEY, algorithm=auth_service.ALGORITHM)
    with pytest.raises(Exception):
        asyncio.run(auth_service.get_current_user(token))
