from django.urls import path
from .views import (
    CustomJWTView,
    RefreshJWTTokenView,
    AdminRegisterAPIView,
    UserRegisterAPIView,
    ChangePasswordView,
    ForgetPasswordView,
    ResetPasswordConfirmView,
    CompaniesListAPIView,
    UserCompaniesListAPIView,
    UpdateUserProfileView,
    UserEmailVerifyView,
    AdminChangeUserPasswordView,
    AddCompanyAPIView,
    CompanyAccessView,
    UsersDeleteAPIView,
    UsersListAPIView,
    CompaniesDeleteAPIView,
    UpdateCompanyAPIView,
    ProfileImageUploadView,
    ProfileImageDestroyView
)


urlpatterns = [
    path('admin/register/', AdminRegisterAPIView.as_view()),
    path('user/register/', UserRegisterAPIView.as_view()),
    path('email/activate/', UserEmailVerifyView.as_view()),
    path('password/reset/', ForgetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPasswordConfirmView.as_view()),
    path('login/', CustomJWTView.as_view(),),
    path('auth/user/', RefreshJWTTokenView.as_view(),),
    path('users/', UsersListAPIView.as_view()),
    path('profile/update/', UpdateUserProfileView.as_view()),
    path('profile/update/image/', ProfileImageUploadView.as_view()),
    path('profile/destroy/image/', ProfileImageDestroyView.as_view()),
    path('password/update/', ChangePasswordView.as_view()),
    path('password/update/user/', AdminChangeUserPasswordView.as_view()),
    path('users/destroy/', UsersDeleteAPIView.as_view()),
    path('company/create/', AddCompanyAPIView.as_view()),
    path('company/update/', UpdateCompanyAPIView.as_view()),
    path('companies/', CompaniesListAPIView.as_view()),
    path('companies/user/', UserCompaniesListAPIView.as_view()),
    path('companies/destroy/', CompaniesDeleteAPIView.as_view()),
    path('company/permission/generate/', CompanyAccessView.as_view())
]
