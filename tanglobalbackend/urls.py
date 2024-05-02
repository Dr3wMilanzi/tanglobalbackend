from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/v1/auth/', include('djoser.urls')),
    path('api/v1/cargo/', include('cargo.urls')),
    path('api/v1/fleet/', include('fleet.urls')),

    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)