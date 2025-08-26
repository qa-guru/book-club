from rest_framework.routers import DefaultRouter

from clubs.api.v1.views import ClubViewSet


router = DefaultRouter()
router.register(r"", ClubViewSet, basename="club")

urlpatterns = router.urls
