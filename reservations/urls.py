from rest_framework import routers
from . import views

app_name = "reservations"

router = routers.DefaultRouter()
router.register("", views.ReservationViewSet)

urlpatterns = router.urls