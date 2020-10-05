from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.get_users),
]