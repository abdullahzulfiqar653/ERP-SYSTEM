from django.urls import path
from .views import (
    ContactCreateAPIView,
    ContactListAPIView,
    ContactsdeleteAPIView,
    ContactUpdateAPIView,
)


urlpatterns = [
    path('create/', ContactCreateAPIView.as_view()),
    path('update/<int:contact_id>/', ContactUpdateAPIView.as_view()),
    path('all/', ContactListAPIView.as_view()),
    path('destroy/', ContactsdeleteAPIView.as_view()),
]
