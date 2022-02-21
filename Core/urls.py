from django.contrib import admin
from django.urls import path
from .views import (
    RegisterAPIView,
    ChangePasswordView
) 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view()),
    path('password/update', ChangePasswordView.as_view(), )
]