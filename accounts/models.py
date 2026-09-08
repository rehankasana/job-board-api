from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        APPLICANT = "APPLICANT", "Applicant"
        RECRUITER = "RECRUITER", "Recruiter"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.APPLICANT
    )

    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.role}"


class ApplicantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applicant_profile"
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=300, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Resume(models.Model):
    applicant = models.OneToOneField(
        ApplicantProfile,
        on_delete=models.CASCADE,
        related_name="resume"
    )

    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.applicant.full_name} Resume"