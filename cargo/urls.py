from django.urls import path
from .views import CargoListCreateAPIView, CargoRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', CargoListCreateAPIView.as_view(), name='cargo-list-create'),
    path('/<uuid:uuid>/', CargoRetrieveUpdateDestroyAPIView.as_view(), name='cargo-detail'),  # Use UUID slug
]
