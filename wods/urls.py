from django.urls import path
from . import views

app_name = "wods"

urlpatterns = [
    path("", views.get_wods),
]