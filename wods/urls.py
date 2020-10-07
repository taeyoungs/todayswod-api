from rest_framework import routers
from . import views

app_name = "wods"

router = routers.DefaultRouter()
router.register("", views.WodViewSet)

urlpatterns = router.urls