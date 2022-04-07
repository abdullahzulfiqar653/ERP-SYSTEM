from django.urls import path
from .views import (
    LookupTypeListAPIView,
    LookupListAPIView,
    TaxListAPIView,
    ChartOfAccountTypeAPIView,
)


urlpatterns = [
    path('type/', LookupTypeListAPIView.as_view()),
    path('<str:lookup>/', LookupListAPIView.as_view()),
    path('tax/<str:lookup>/', TaxListAPIView.as_view()),
    path('chartofaccount/<str:lookup>/', ChartOfAccountTypeAPIView.as_view()),
]
