from django.contrib import admin
from django.urls import path, include
from .views import (
    RegisterAPIView,
    ChangePasswordView,
    CustomJWTView,
    ForgetPasswordView,
    ResetPsswordConfirmView
)



urlpatterns = [
    path('login/', CustomJWTView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPIView.as_view()),
    path('password/update/', ChangePasswordView.as_view()),
    path('password/reset/', ForgetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPsswordConfirmView.as_view())
]