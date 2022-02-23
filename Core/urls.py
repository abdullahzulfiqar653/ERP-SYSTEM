from django.urls import path
from .views import (
    RegisterAPIView,
    CustomJWTView,
    ChangePasswordView,
    ForgetPasswordView,
    ResetPsswordConfirmView,
    CompaniesListAPIView,
)



urlpatterns = [
    path('login/', CustomJWTView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPIView.as_view()),
    path('password/update/', ChangePasswordView.as_view()),
    path('password/reset/', ForgetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPsswordConfirmView.as_view()),
    path('companies/', CompaniesListAPIView.as_view())
]