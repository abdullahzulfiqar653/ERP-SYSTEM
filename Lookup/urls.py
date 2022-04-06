from django.urls import path
from .views import (
    LookupTypeListAPIView,
    LookupListAPIView,
    TaxListAPIView,
)


urlpatterns = [
    path('type/', LookupTypeListAPIView.as_view()),
    path('<str:lookup>/', LookupListAPIView.as_view()),
    path('tax/<str:lookup>/', TaxListAPIView.as_view()),
]
