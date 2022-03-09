from django.urls import path
from .views import (
    AdminRegisterAPIView,
    UserRegisterAPIView,
    CustomJWTView,
    RefreshJWTTokenView,
    ChangePasswordView,
    ForgetPasswordView,
    ResetPsswordConfirmView,
    CompaniesListAPIView,
    UserProfileUpdateView,
    FetchUserProfileView,
    UserDeleteAPIView,
    UserEmailVerifyView,
    AdminChangeUserPasswordView,
    AddCompanyAPIView,
    CompanyAccessView,
    
)



urlpatterns = [
    path('login/', CustomJWTView.as_view(),),
    path('users/', RefreshJWTTokenView.as_view(),),

    path('admin/register/', AdminRegisterAPIView.as_view()),
    path('user/register/', UserRegisterAPIView.as_view()),

    path('email/activate/', UserEmailVerifyView.as_view()),

    path('password/update/', ChangePasswordView.as_view()),
    path('user/password/update/', AdminChangeUserPasswordView.as_view()),

    path('password/reset/', ForgetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPsswordConfirmView.as_view()),

    path('companies/', CompaniesListAPIView.as_view()),
    path('profile/update/', UserProfileUpdateView.as_view()),
    path('profile/<pk>/', FetchUserProfileView.as_view()),

    path('user/destroy/<pk>/', UserDeleteAPIView.as_view()),

    path('company/create/', AddCompanyAPIView.as_view()),

    path('user/access/company/', CompanyAccessView.as_view())
]