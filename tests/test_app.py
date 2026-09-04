import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_home(client):
    response=client.get(reverse("web:home"))
    assert response.status_code==200

def test_content_api(client,content):
    response=client.get("/api/v1/contents/")
    assert response.status_code==200
    assert response.json()["count"]==1

def test_content_page(client,content):
    response=client.get(reverse("web:content_detail",args=[content.slug]))
    assert response.status_code==200
    assert content.title in response.content.decode()

def test_draft_hidden(client,content):
    content.status="draft";content.save()
    assert client.get("/api/v1/contents/").json()["count"]==0


def test_register_login_and_account(client, db):
    response = client.post(reverse("web:register"), {
        "full_name": "مستخدم جديد",
        "email": "member@example.com",
        "password1": "SafePassword123!",
        "password2": "SafePassword123!",
    })
    assert response.status_code == 302
    assert response.url == reverse("web:account")
    assert client.get(reverse("web:account")).status_code == 200


def test_guest_progress_is_saved_in_session(client, content):
    response = client.post(reverse("web:progress", args=[content.slug]), {"position": 48, "total": 120})
    assert response.status_code == 200
    assert response.json()["progress_percent"] == 40
