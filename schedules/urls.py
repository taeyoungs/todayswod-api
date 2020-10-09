from rest_framework import routers
from . import views

app_name = "schedules"

router = routers.DefaultRouter()
router.register("", views.ScheduleViewSet)

urlpatterns = router.urls