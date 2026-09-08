from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Job
from .serializers import JobSerializer


class JobPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "company",
        "location",
        "skills",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "salary_min",
        "salary_max",
        "deadline",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Job.objects.filter(
            is_active=True
        )

        employment_type = self.request.query_params.get(
            "employment_type"
        )

        if employment_type:
            queryset = queryset.filter(
                employment_type=employment_type
            )

        location = self.request.query_params.get(
            "location"
        )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        return queryset

    def perform_create(self, serializer):
        if self.request.user.role != "RECRUITER":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only recruiters can create jobs."
            )

        serializer.save(
            recruiter=self.request.user
        )


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()

    def perform_update(self, serializer):
        if self.request.user.role != "RECRUITER":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only recruiters can update jobs."
            )

        if serializer.instance.recruiter != self.request.user:
            raise PermissionDenied(
                "You can only update your own jobs."
            )

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "RECRUITER":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only recruiters can delete jobs."
            )

        if instance.recruiter != self.request.user:
            raise PermissionDenied(
                "You can only delete your own jobs."
            )

        instance.delete()