from django.urls import path
from .views import CargoListCreateAPIView, CargoRetrieveUpdateDestroyAPIView, CargoByCategoryAPIView,CargoCartegoriesCreateAPIView

urlpatterns = [
    path('', CargoListCreateAPIView.as_view(), name='cargo-list-create'),
    path('type', CargoCartegoriesCreateAPIView.as_view(), name='cargo-list-create'),
    path('<uuid:uuid>', CargoRetrieveUpdateDestroyAPIView.as_view(), name='cargo-retrieve-update-destroy'),
    path('by-category', CargoByCategoryAPIView.as_view(), name='cargo-by-category'),
]