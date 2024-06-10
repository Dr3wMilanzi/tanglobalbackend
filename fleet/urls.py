from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleCreateList,VehicleTypeView,VehicleDetail,ApproveVehicleView



urlpatterns = [
    # path('', include(router.urls)),
    path('',VehicleCreateList.as_view(),name="vehicles"),
    path("<int:pk>/",VehicleDetail.as_view(), name="vehicle-detail"),
    path('<int:pk>/approve/', ApproveVehicleView.as_view(), name='vehicle-approve'),
    path('type', VehicleTypeView.as_view(), name='vehicle-type'),
]
