from rest_framework.routers import DefaultRouter
from .views import PageViewSet, PostViewSet, TagViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("tags", TagViewSet, basename="tag")
router.register("pages", PageViewSet, basename="page")

urlpatterns = router.urls