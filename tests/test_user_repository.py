import pytest
from app.repository import user_repository
from app.dto.user import UserDTO


def test_create_user_success(monkeypatch):
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def add(self, obj):
            pass

        def commit(self):
            pass

    monkeypatch.setattr(user_repository, "SessionLocal", lambda: FakeSession())
    user = UserDTO(
        username="testuser",
        email="test@user.com",
        first_name="Test",
        last_name="User",
        password="123456",
        role="user",
        phone_number="123456789",
    )
    user_repository.create_user(user)


def test_create_user_integrity(monkeypatch):
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def add(self, obj):
            pass

        def commit(self):
            raise user_repository.IntegrityError("error", None, None)

        def rollback(self):
            pass

    monkeypatch.setattr(user_repository, "SessionLocal", lambda: FakeSession())
    user = UserDTO(
        username="testuser",
        email="test@user.com",
        first_name="Test",
        last_name="User",
        password="123456",
        role="user",
        phone_number="123456789",
    )
    with pytest.raises(Exception):
        user_repository.create_user(user)


def test_create_user_unexpected(monkeypatch):
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def add(self, obj):
            raise Exception("fail")

        def commit(self):
            pass

        def rollback(self):
            pass

    monkeypatch.setattr(user_repository, "SessionLocal", lambda: FakeSession())
    user = UserDTO(
        username="testuser",
        email="test@user.com",
        first_name="Test",
        last_name="User",
        password="123456",
        role="user",
        phone_number="123456789",
    )
    with pytest.raises(Exception):
        user_repository.create_user(user)


def test_authenticate_user_success(monkeypatch):
    class FakeUser:
        hashed_password = user_repository.bcrypt_context.hash("123456")

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def query(self, model):
            return self

        def filter(self, *args):
            return self

        def first(self):
            return FakeUser()

    monkeypatch.setattr(user_repository, "SessionLocal", lambda: FakeSession())
    assert user_repository.authenticate_user("testuser", "123456")


def test_authenticate_user_fail(monkeypatch):
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def query(self, model):
            return self

        def filter(self, *args):
            return self

        def first(self):
            return None

    monkeypatch.setattr(user_repository, "SessionLocal", lambda: FakeSession())
    assert user_repository.authenticate_user("testuser", "wrong") is False
