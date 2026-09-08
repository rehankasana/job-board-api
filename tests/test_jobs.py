import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from jobs.models import Job

User = get_user_model()


@pytest.fixture
def recruiter():
    return User.objects.create_user(
        username="recruiter",
        email="recruiter@test.com",
        password="TestPassword123",
        role="RECRUITER",
    )


@pytest.fixture
def applicant():
    return User.objects.create_user(
        username="applicant",
        email="applicant@test.com",
        password="TestPassword123",
        role="APPLICANT",
    )


@pytest.fixture
def recruiter_client(recruiter):
    client = APIClient()
    client.force_authenticate(user=recruiter)
    return client


@pytest.fixture
def applicant_client(applicant):
    client = APIClient()
    client.force_authenticate(user=applicant)
    return client


@pytest.fixture
def job(recruiter):
    return Job.objects.create(
        recruiter=recruiter,
        title="Django Developer",
        company="Tech Solutions",
        description="Django REST API developer",
        location="Lahore",
        skills="Python, Django, DRF",
        employment_type="FULL_TIME",
        salary_min=100000,
        salary_max=180000,
        deadline="2026-12-31",
        is_active=True,
    )


@pytest.mark.django_db
def test_recruiter_can_create_job(recruiter_client):

    response = recruiter_client.post(
        "/api/jobs/",
        {
            "title": "Backend Developer",
            "company": "ABC Technologies",
            "description": "Build Django APIs",
            "location": "Lahore",
            "skills": "Python, Django, REST API",
            "employment_type": "FULL_TIME",
            "salary_min": 100000,
            "salary_max": 200000,
            "deadline": "2026-12-31",
            "is_active": True,
        },
        format="json",
    )

    assert response.status_code == 201
    assert Job.objects.count() == 1
    assert Job.objects.first().recruiter == recruiter_client.handler._force_user


@pytest.mark.django_db
def test_applicant_cannot_create_job(applicant_client):

    response = applicant_client.post(
        "/api/jobs/",
        {
            "title": "Django Developer",
            "company": "ABC Technologies",
            "description": "Build Django APIs",
            "location": "Lahore",
            "skills": "Python, Django",
            "employment_type": "FULL_TIME",
            "deadline": "2026-12-31",
            "is_active": True,
        },
        format="json",
    )

    assert response.status_code == 403
    assert Job.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_list_jobs(
    applicant_client,
    job,
):

    response = applicant_client.get(
        "/api/jobs/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "Django Developer"


@pytest.mark.django_db
def test_job_search(applicant_client, job):

    response = applicant_client.get(
        "/api/jobs/?search=Django"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_job_location_filter(applicant_client, job):

    response = applicant_client.get(
        "/api/jobs/?location=Lahore"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_job_employment_type_filter(
    applicant_client,
    job,
):

    response = applicant_client.get(
        "/api/jobs/?employment_type=FULL_TIME"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_recruiter_can_update_own_job(
    recruiter_client,
    job,
):

    response = recruiter_client.patch(
        f"/api/jobs/{job.id}/",
        {
            "title": "Senior Django Developer"
        },
        format="json",
    )

    assert response.status_code == 200

    job.refresh_from_db()

    assert job.title == "Senior Django Developer"


@pytest.mark.django_db
def test_applicant_cannot_update_job(
    applicant_client,
    job,
):

    response = applicant_client.patch(
        f"/api/jobs/{job.id}/",
        {
            "title": "Hacked Job"
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_recruiter_can_delete_own_job(
    recruiter_client,
    job,
):

    response = recruiter_client.delete(
        f"/api/jobs/{job.id}/"
    )

    assert response.status_code == 204
    assert not Job.objects.filter(
        id=job.id
    ).exists()