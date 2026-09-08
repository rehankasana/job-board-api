from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(
        source="applicant.full_name",
        read_only=True
    )

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company = serializers.CharField(
        source="job.company",
        read_only=True
    )

    resume_file = serializers.FileField(
        source="resume.file",
        read_only=True
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "job",
            "job_title",
            "company",
            "applicant",
            "applicant_name",
            "resume",
            "resume_file",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "applicant",
            "applicant_name",
            "job_title",
            "company",
            "resume",
            "resume_file",
            "status",
            "applied_at",
            "updated_at",
        ]

class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ["status"]

    def validate_status(self, value):
        allowed_statuses = [
            Application.Status.APPLIED,
            Application.Status.REVIEWING,
            Application.Status.SHORTLISTED,
            Application.Status.REJECTED,
            Application.Status.HIRED,
        ]

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                "Invalid application status."
            )

        return value