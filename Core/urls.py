from django.urls import path
from .views import (
    RegisterAPIView,
    CustomJWTView,
    ChangePasswordView,
    ForgetPasswordView,
    ResetPsswordConfirmView,
    CompaniesListAPIView,
    UserProfileUpdateView,
    CompanyDeleteAPIView,
    UserEmailVerifyView
)



urlpatterns = [
    path('login/', CustomJWTView.as_view(),),
    path('register/', RegisterAPIView.as_view()),
    path('email/activate/', UserEmailVerifyView.as_view()),
    path('password/update/', ChangePasswordView.as_view()),
    path('password/reset/', ForgetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPsswordConfirmView.as_view()),
    path('companies/', CompaniesListAPIView.as_view()),
    path('profile/update/', UserProfileUpdateView.as_view()),
    path('company/destroy/<pk>/', CompanyDeleteAPIView.as_view())
]