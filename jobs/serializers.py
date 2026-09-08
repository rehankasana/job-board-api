from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(
        source="recruiter.username",
        read_only=True
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "recruiter",
            "recruiter_name",
            "title",
            "company",
            "description",
            "location",
            "skills",
            "employment_type",
            "salary_min",
            "salary_max",
            "deadline",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "recruiter",
            "recruiter_name",
            "created_at",
            "updated_at",
        ]