from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, GroupJoinRequestViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'join-requests', GroupJoinRequestViewSet, basename='join-request')

urlpatterns = router.urls
