from rest_framework import routers
from . import views

app_name = "memberships"

router = routers.DefaultRouter()
router.register("", views.MembershipViewSet)

urlpatterns = router.urls