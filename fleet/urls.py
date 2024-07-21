from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleTypeViewSet, VehicleViewSet, DriverViewSet, TripViewSet, VehicleImageViewSet

router = DefaultRouter()
router.register(r'type', VehicleTypeViewSet, basename='vehicle-type')
router.register(r'', VehicleViewSet, basename='vehicle')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'trips', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
]
