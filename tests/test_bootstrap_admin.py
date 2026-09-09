from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

pytestmark = pytest.mark.django_db
PASSWORD = "Example-test-only-9!abc"


@pytest.fixture(autouse=True)
def clear_bootstrap_env(monkeypatch):
    monkeypatch.delenv("ZAOUIA_ADMIN_EMAIL", raising=False)
    monkeypatch.delenv("ZAOUIA_ADMIN_PASSWORD", raising=False)


def configure(monkeypatch, email="owner@example.test", password=PASSWORD):
    monkeypatch.setenv("ZAOUIA_ADMIN_EMAIL", email)
    monkeypatch.setenv("ZAOUIA_ADMIN_PASSWORD", password)


def test_unconfigured_bootstrap_is_noop():
    call_command("bootstrap_admin")
    assert not get_user_model().objects.exists()


def test_missing_password_fails_without_user(monkeypatch):
    monkeypatch.setenv("ZAOUIA_ADMIN_EMAIL", "owner@example.test")
    with pytest.raises(CommandError):
        call_command("bootstrap_admin")
    assert not get_user_model().objects.exists()


@pytest.mark.parametrize("email,password", [
    ("invalid", PASSWORD),
    ("owner@example.test", "short"),
    ("owner@example.test", "password12345"),
])
def test_invalid_credentials_rejected(monkeypatch, email, password):
    configure(monkeypatch, email, password)
    with pytest.raises(CommandError):
        call_command("bootstrap_admin")
    assert not get_user_model().objects.exists()


def test_creates_admin_with_hashed_password_without_logging_secret(monkeypatch):
    configure(monkeypatch)
    output = StringIO()
    call_command("bootstrap_admin", stdout=output)
    user = get_user_model().objects.get()
    assert user.is_active and user.is_staff and user.is_superuser
    assert user.role == "admin"
    assert user.check_password(PASSWORD)
    assert user.password != PASSWORD
    assert PASSWORD not in output.getvalue()


def test_rerun_does_not_reset_password(monkeypatch):
    configure(monkeypatch)
    call_command("bootstrap_admin")
    original = get_user_model().objects.get().password
    configure(monkeypatch, email="OWNER@example.test", password="Different-test-123!")
    call_command("bootstrap_admin")
    assert get_user_model().objects.count() == 1
    assert get_user_model().objects.get().password == original


def test_existing_member_not_promoted(monkeypatch):
    User = get_user_model()
    user = User.objects.create_user(email="owner@example.test", password=PASSWORD)
    configure(monkeypatch)
    with pytest.raises(CommandError):
        call_command("bootstrap_admin")
    user.refresh_from_db()
    assert not user.is_superuser and not user.is_staff
    assert user.role == "member"


def test_second_admin_refused(monkeypatch):
    User = get_user_model()
    User.objects.create_superuser(email="first@example.test", password=PASSWORD)
    configure(monkeypatch)
    with pytest.raises(CommandError):
        call_command("bootstrap_admin")
    assert User.objects.count() == 1
