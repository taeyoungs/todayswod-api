from rest_framework import routers
from .views import AlertViewSet

app_name = "alerts"

router = routers.DefaultRouter()
router.register("", AlertViewSet)

urlpatterns = router.urls