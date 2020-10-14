from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls", namespace="users")),
    path("api/v1/boxes/", include("boxes.urls", namespace="boxes")),
    path("api/v1/wods/", include("wods.urls", namespace="wods")),
    path("api/v1/memberships/", include("memberships.urls", namespace="memberships")),
    path("api/v1/schedules/", include("schedules.urls", namespace="schedules")),
    path(
        "api/v1/reservations/", include("reservations.urls", namespace="reservations")
    ),
    path("api/v1/alerts/", include("alerts.urls", namespace="alerts")),
]
