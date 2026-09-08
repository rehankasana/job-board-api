from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from accounts.models import ApplicantProfile, Resume
from jobs.models import Job

from .models import Application
from .serializers import ApplicationSerializer
from .serializers import (
    ApplicationSerializer,
    ApplicationStatusSerializer,
)
class ApplicationPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        if self.request.user.role != "APPLICANT":
            raise PermissionDenied(
                "Only applicants can apply for jobs."
            )

        job_id = self.request.data.get("job")

        job = get_object_or_404(
            Job,
            id=job_id,
            is_active=True
        )

        profile = get_object_or_404(
            ApplicantProfile,
            user=self.request.user
        )

        resume = getattr(profile, "resume", None)

        if not resume:
            raise PermissionDenied(
                "You must upload a resume before applying."
            )

        if Application.objects.filter(
            job=job,
            applicant=profile
        ).exists():
            raise PermissionDenied(
                "You have already applied for this job."
            )

        serializer.save(
            job=job,
            applicant=profile,
            resume=resume
        )


class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        if self.request.user.role != "APPLICANT":
            raise PermissionDenied(
                "Only applicants can view their applications."
            )

        return Application.objects.filter(
            applicant__user=self.request.user
        ).select_related("job", "applicant", "resume")

class ApplicationDetailView(
    generics.RetrieveDestroyAPIView
):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.role == "APPLICANT":
            return Application.objects.filter(
                applicant__user=self.request.user
            )

        if self.request.user.role == "RECRUITER":
            return Application.objects.filter(
                job__recruiter=self.request.user
            )

        return Application.objects.none()
class RecruiterApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        if self.request.user.role != "RECRUITER":
            raise PermissionDenied(
                "Only recruiters can view received applications."
            )

        return Application.objects.filter(
            job__recruiter=self.request.user
        ).select_related("job", "applicant", "resume")
    
class RecruiterApplicationStatusView(
    generics.UpdateAPIView
):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ["patch"]

    def get_queryset(self):

        if self.request.user.role != "RECRUITER":
            raise PermissionDenied(
                "Only recruiters can update application status."
            )

        return Application.objects.filter(
            job__recruiter=self.request.user
        )   