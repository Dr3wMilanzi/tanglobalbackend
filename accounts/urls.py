from django.urls import path, include
from . import views



urlpatterns = [
    # path('', include(router.urls)),
    path('',views.CompanyCreateList.as_view(),name="company"),
    path('<int:pk>',views.CompanyRetrieve.as_view(),name="company-details")
]
