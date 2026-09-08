from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "location",
        "employment_type",
        "is_active",
        "deadline",
        "created_at",
    )

    list_filter = (
        "employment_type",
        "is_active",
        "location",
    )

    search_fields = (
        "title",
        "company",
        "skills",
        "location",
    )