from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleCreateList,VehicleTypeView



urlpatterns = [
    # path('', include(router.urls)),
    path('',VehicleCreateList.as_view(),name="vehicles"),
    path('type', VehicleTypeView.as_view(), name='vehicle-type'),
]
