import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import ApplicantProfile, Resume
from applications.models import Application
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
def applicant_profile(applicant):
    return ApplicantProfile.objects.create(
        user=applicant,
        full_name="Test Applicant",
        location="Lahore",
        skills="Python, Django, DRF",
    )


@pytest.fixture
def resume(applicant_profile):
    return Resume.objects.create(
        applicant=applicant_profile,
        file="resumes/test_resume.pdf",
    )


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


@pytest.fixture
def applicant_client(applicant):
    client = APIClient()
    client.force_authenticate(user=applicant)
    return client


@pytest.fixture
def recruiter_client(recruiter):
    client = APIClient()
    client.force_authenticate(user=recruiter)
    return client


@pytest.mark.django_db
def test_applicant_can_apply(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "I am interested in this position.",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Application.objects.count() == 1

    application = Application.objects.first()

    assert application.job == job
    assert application.applicant == applicant_profile
    assert application.resume == resume
    assert application.status == "APPLIED"


@pytest.mark.django_db
def test_applicant_cannot_apply_without_resume(
    applicant_client,
    applicant_profile,
    job,
):
    response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "I am interested.",
        },
        format="json",
    )

    assert response.status_code == 403
    assert Application.objects.count() == 0


@pytest.mark.django_db
def test_applicant_cannot_apply_twice(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    first_response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "First application.",
        },
        format="json",
    )

    assert first_response.status_code == 201

    second_response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "Second application.",
        },
        format="json",
    )

    assert second_response.status_code == 403
    assert Application.objects.count() == 1


@pytest.mark.django_db
def test_applicant_can_view_own_applications(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
        cover_letter="Test application.",
    )

    response = applicant_client.get(
        "/api/applications/my/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert (
        response.data["results"][0]["job_title"]
        == "Django Developer"
    )


@pytest.mark.django_db
def test_recruiter_can_view_received_applications(
    recruiter_client,
    applicant_profile,
    resume,
    job,
):
    Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
        cover_letter="Test application.",
    )

    response = recruiter_client.get(
        "/api/applications/received/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_recruiter_can_update_application_status(
    recruiter_client,
    applicant_profile,
    resume,
    job,
):
    application = Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
        cover_letter="Test application.",
    )

    response = recruiter_client.patch(
        f"/api/applications/{application.id}/status/",
        {
            "status": "SHORTLISTED"
        },
        format="json",
    )

    assert response.status_code == 200

    application.refresh_from_db()

    assert application.status == "SHORTLISTED"


@pytest.mark.django_db
def test_applicant_cannot_update_application_status(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    application = Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
    )

    response = applicant_client.patch(
        f"/api/applications/{application.id}/status/",
        {
            "status": "HIRED"
        },
        format="json",
    )

    assert response.status_code == 403

    application.refresh_from_db()

    assert application.status == "APPLIED"

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import ApplicantProfile, Resume
from applications.models import Application
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
def applicant_profile(applicant):
    return ApplicantProfile.objects.create(
        user=applicant,
        full_name="Test Applicant",
        location="Lahore",
        skills="Python, Django, DRF",
    )


@pytest.fixture
def resume(applicant_profile):
    return Resume.objects.create(
        applicant=applicant_profile,
        file="resumes/test_resume.pdf",
    )


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


@pytest.fixture
def applicant_client(applicant):
    client = APIClient()
    client.force_authenticate(user=applicant)
    return client


@pytest.fixture
def recruiter_client(recruiter):
    client = APIClient()
    client.force_authenticate(user=recruiter)
    return client


@pytest.mark.django_db
def test_applicant_can_apply(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "I am interested in this position.",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Application.objects.count() == 1

    application = Application.objects.first()

    assert application.job == job
    assert application.applicant == applicant_profile
    assert application.resume == resume
    assert application.status == "APPLIED"


@pytest.mark.django_db
def test_applicant_cannot_apply_without_resume(
    applicant_client,
    applicant_profile,
    job,
):
    response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "I am interested.",
        },
        format="json",
    )

    assert response.status_code == 403
    assert Application.objects.count() == 0


@pytest.mark.django_db
def test_applicant_cannot_apply_twice(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    first_response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "First application.",
        },
        format="json",
    )

    assert first_response.status_code == 201

    second_response = applicant_client.post(
        "/api/applications/",
        {
            "job": job.id,
            "cover_letter": "Second application.",
        },
        format="json",
    )

    assert second_response.status_code == 403
    assert Application.objects.count() == 1


@pytest.mark.django_db
def test_applicant_can_view_own_applications(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
        cover_letter="Test application.",
    )

    response = applicant_client.get(
        "/api/applications/my/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert (
        response.data["results"][0]["job_title"]
        == "Django Developer"
    )


@pytest.mark.django_db
def test_recruiter_can_view_received_applications(
    recruiter_client,
    applicant_profile,
    resume,
    job,
):
    Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
        cover_letter="Test application.",
    )

    response = recruiter_client.get(
        "/api/applications/received/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_recruiter_can_update_application_status(
    recruiter_client,
    applicant_profile,
    resume,
    job,
):
    application = Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
        cover_letter="Test application.",
    )

    response = recruiter_client.patch(
        f"/api/applications/{application.id}/status/",
        {
            "status": "SHORTLISTED"
        },
        format="json",
    )

    assert response.status_code == 200

    application.refresh_from_db()

    assert application.status == "SHORTLISTED"


@pytest.mark.django_db
def test_applicant_cannot_update_application_status(
    applicant_client,
    applicant_profile,
    resume,
    job,
):
    application = Application.objects.create(
        job=job,
        applicant=applicant_profile,
        resume=resume,
    )

    response = applicant_client.patch(
        f"/api/applications/{application.id}/status/",
        {
            "status": "HIRED"
        },
        format="json",
    )

    assert response.status_code == 403

    application.refresh_from_db()

    assert application.status == "APPLIED"