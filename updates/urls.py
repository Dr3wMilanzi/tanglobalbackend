# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('update-types/', views.UpdateTypeList.as_view(), name='update-type-list'),
    path('update-types/<int:pk>/', views.UpdateTypeDetail.as_view(), name='update-type-detail'),
    path('', views.UpdateList.as_view(), name='update-list'),
    path('<slug:slug>/approve/', views.ApproveUpdateView.as_view(), name='update-approve'),
    path('<slug:slug>/', views.UpdateDetail.as_view(), name='update-detail'),
    path('mine/categories/', views.UserSelectedUpdatesList.as_view(), name='my-subscription-list'),
    path('mine/', views.UserSubscriptionList.as_view(), name='user-subscription-list'),
    # path('my-subscriptions/<int:pk>/', views.UserSubscriptionDetail.as_view(), name='user-subscription-detail'),
    path('viewed/', views.UpdateViewList.as_view(), name='update-view-list'),
]
