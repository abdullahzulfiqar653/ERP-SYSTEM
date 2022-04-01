from django.urls import path
from .views import (
    AddTeamView,
    TeamListView,
    UpdateTeamView,
    TeamDestroyView,
    EmployeeUpdateView,
    EmployeeCreateAPIView,
    EmployeeListAPIView,
    EmployeeDestroyView,

    PayRollCreateAPIView,
    PayRollListAPIView,
    PayRollItemListAPIView,
    PayRollDestroyView,
    PayRollItemDestroyView,
    PayRollItemUpdateAPIView,
    ContactCreateAPIView,
    ContactListAPIView,
    ContactsdeleteAPIView,
    ContactUpdateAPIView,

    LookupTypeListAPIView,
    LookupListAPIView,
    TaxListAPIView,
)


urlpatterns = [
    path('team/add/', AddTeamView.as_view()),
    path('teams/', TeamListView.as_view()),
    path('team/update/<int:team_id>/', UpdateTeamView.as_view()),
    path('team/destroy/<pk>/', TeamDestroyView.as_view()),

    path('employee/add/', EmployeeCreateAPIView.as_view()),
    path('employee/update/<int:emp_id>/', EmployeeUpdateView.as_view()),
    path('employees/', EmployeeListAPIView.as_view()),
    path('employee/destroy/<pk>/', EmployeeDestroyView.as_view()),

    path('create/', PayRollCreateAPIView.as_view()),
    path('items/update/<int:payroll_id>/', PayRollItemUpdateAPIView.as_view()),
    path('all/', PayRollListAPIView.as_view()),
    path('items/<pk>/', PayRollItemListAPIView.as_view()),
    path('destroy/<pk>/', PayRollDestroyView.as_view()),
    path('item/destroy/<pk>/', PayRollItemDestroyView.as_view()),

    path('contact/add/', ContactCreateAPIView.as_view()),
    path('contact/update/<int:contact_id>/', ContactUpdateAPIView.as_view()),
    path('contacts/', ContactListAPIView.as_view()),
    path('contacts/destroy/', ContactsdeleteAPIView.as_view()),
]

# ---------------------------------------------------------------------------------#
# ---------------------- URLS for Lookups Module ---------------------------------#
# ---------------------------------------------------------------------------------#
urlpatterns += [
    path('lookup/type/', LookupTypeListAPIView.as_view()),
    path('lookups/<str:lookup>/', LookupListAPIView.as_view()),
    path('lookup/tax/<str:lookup>/', TaxListAPIView.as_view()),
]
