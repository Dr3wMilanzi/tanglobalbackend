from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargoTypeViewSet, CargoViewSet, CargoDocumentViewSet, CargoImageViewSet, CargoTrackingViewSet

router = DefaultRouter()
router.register(r'type/cargo', CargoTypeViewSet)
router.register(r'', CargoViewSet)
router.register(r'cargo-documents', CargoDocumentViewSet)
router.register(r'cargo-images', CargoImageViewSet)
router.register(r'cargo-tracking', CargoTrackingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from .views import CargoTypeViewSet, CargoViewSet, CargoDocumentViewSet, CargoImageViewSet, CargoTrackingViewSet

# router = DefaultRouter()
# router.register(r'cargo-types', CargoTypeViewSet)
# router.register(r'cargos', CargoViewSet)
# router.register(r'cargo-documents', CargoDocumentViewSet)
# router.register(r'cargo-images', CargoImageViewSet)
# router.register(r'cargo-tracking', CargoTrackingViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]