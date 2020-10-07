from rest_framework import routers
from . import views

app_name = "boxes"

router = routers.DefaultRouter()
router.register("", views.BoxViewSet)

urlpatterns = router.urls