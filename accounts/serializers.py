from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ApplicantProfile, Resume
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
        ]

class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = [
            "id",
            "file",
            "uploaded_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_at",
            "updated_at",
        ]

    def validate_file(self, value):
        allowed_extensions = [
            ".pdf",
            ".doc",
            ".docx",
        ]

        extension = value.name.lower().split(".")[-1]

        if f".{extension}" not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOC, and DOCX files are allowed."
            )

        max_size = 5 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                "Resume file must be smaller than 5 MB."
            )

        return value       