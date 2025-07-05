from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MotherViewSet,
    SaplingViewSet,
    HealthWorkerViewSet,
    ReminderLogViewSet,
    PhotoUploadViewSet,
)

router = DefaultRouter()
router.register(r'mothers', MotherViewSet)
router.register(r'saplings', SaplingViewSet)
router.register(r'health-workers', HealthWorkerViewSet)
router.register(r'reminder-logs', ReminderLogViewSet)
router.register(r'photo-uploads', PhotoUploadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
