from django.urls import path
from .views import (
    LookupTypeListAPIView,
    LookupListAPIView,
    PayrollTaxListAPIView,
    ContactTaxListAPIView,
    ChartOfAccountTypeAPIView,
)


urlpatterns = [
    path('type/', LookupTypeListAPIView.as_view()),
    path('<str:lookup>/', LookupListAPIView.as_view()),
    path('tax/<str:lookup>/', PayrollTaxListAPIView.as_view()),
    path('tax/contact/<int:lookup>/', ContactTaxListAPIView.as_view()),
    path('chartofaccount/<str:lookup>/', ChartOfAccountTypeAPIView.as_view()),
]
