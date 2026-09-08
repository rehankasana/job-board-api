from django.urls import path

from .views import (
    ApplicationCreateView,
    MyApplicationsView,
    ApplicationDetailView,
    RecruiterApplicationsView,
    RecruiterApplicationStatusView,
)

urlpatterns = [
    path("", ApplicationCreateView.as_view(), name="application-create"),
    path("my/", MyApplicationsView.as_view(), name="my-applications"),
    path(
        "received/",
        RecruiterApplicationsView.as_view(),
        name="received-applications",
    ),
    path(
        "<int:pk>/status/",
        RecruiterApplicationStatusView.as_view(),
        name="application-status",
    ),
    path(
        "<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail",
    ),
]