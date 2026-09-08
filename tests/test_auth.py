import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_applicant_registration():
    client = APIClient()

    response = client.post(
        "/api/auth/register/",
        {
            "username": "testapplicant",
            "email": "applicant@test.com",
            "password": "TestPassword123",
            "role": "APPLICANT",
        },
        format="json",
    )

    assert response.status_code == 201
    assert User.objects.filter(
        username="testapplicant"
    ).exists()


@pytest.mark.django_db
def test_recruiter_registration():
    client = APIClient()

    response = client.post(
        "/api/auth/register/",
        {
            "username": "testrecruiter",
            "email": "recruiter@test.com",
            "password": "TestPassword123",
            "role": "RECRUITER",
        },
        format="json",
    )

    assert response.status_code == 201

    user = User.objects.get(
        username="testrecruiter"
    )

    assert user.role == "RECRUITER"


@pytest.mark.django_db
def test_login_returns_jwt_tokens():
    user = User.objects.create_user(
        username="loginuser",
        email="login@test.com",
        password="TestPassword123",
        role="APPLICANT",
    )

    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {
            "username": "loginuser",
            "password": "TestPassword123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data