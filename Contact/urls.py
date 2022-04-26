from django.urls import path
from .views import (
    ContactCreateAPIView,
    ContactsdeleteAPIView,
    ContactUpdateAPIView,
    ContactRetrieveAPIView,
    ContactListAPIView,
    ContactListForExpenseView,
    ContactListForInvoiceDropdownAPIView,
    ContactRetrieveForInvoiceAPIView
)


urlpatterns = [
    path('create/', ContactCreateAPIView.as_view()),
    path('retrieve/<pk>/', ContactRetrieveAPIView.as_view()),
    path('update/<int:contact_id>/', ContactUpdateAPIView.as_view()),
    path('all/', ContactListAPIView.as_view()),
    path('destroy/', ContactsdeleteAPIView.as_view()),
    path('expense/<str:lookup>/', ContactListForExpenseView.as_view()),
    path('invoice/', ContactListForInvoiceDropdownAPIView.as_view()),
    path('invoice/<pk>/', ContactRetrieveForInvoiceAPIView.as_view())
]
