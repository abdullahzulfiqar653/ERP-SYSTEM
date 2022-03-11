from django.urls import path
from .views import (
    CustomJWTView,
    RefreshJWTTokenView,

    AdminRegisterAPIView,
    UserRegisterAPIView,
    
    ChangePasswordView,
    ForgetPasswordView,
    ResetPsswordConfirmView,
    CompaniesListAPIView,
    UserCompaniesListAPIView,
    UpdateUserProfileView,
    FetchUserProfileView,
    
    UserEmailVerifyView,
    AdminChangeUserPasswordView,
    AddCompanyAPIView,
    CompanyAccessView,

    UserDeleteAPIView,
    CompanyDeleteAPIView,

    UpdateCompanyAPIView,
)



urlpatterns = [
    path('admin/register/', AdminRegisterAPIView.as_view()),
    path('user/register/', UserRegisterAPIView.as_view()),
    
    path('email/activate/', UserEmailVerifyView.as_view()),

    path('password/reset/', ForgetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPsswordConfirmView.as_view()),

    path('login/', CustomJWTView.as_view(),),
    path('auth/user/', RefreshJWTTokenView.as_view(),),

    path('profile/', FetchUserProfileView.as_view()),
    path('profile/update/', UpdateUserProfileView.as_view()),

    path('password/update/', ChangePasswordView.as_view()),
    path('password/update/user/', AdminChangeUserPasswordView.as_view()),

    path('user/destroy/<pk>/', UserDeleteAPIView.as_view()),

    path('company/create/', AddCompanyAPIView.as_view()),
    path('company/update/', UpdateCompanyAPIView.as_view()),
    path('companies/', CompaniesListAPIView.as_view()),
    path('companies/user/', UserCompaniesListAPIView.as_view()),
    path('company/destroy/<pk>/', CompanyDeleteAPIView.as_view()),
    path('company/permission/generate/', CompanyAccessView.as_view())
]