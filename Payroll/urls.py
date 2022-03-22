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
    PayRollItemUpdateAPIView
)


urlpatterns = [
    path('team/add/', AddTeamView.as_view()),
    path('teams/', TeamListView.as_view()),
    path('team/update/<int:id>/', UpdateTeamView.as_view()),
    path('team/destroy/<pk>/', TeamDestroyView.as_view()),

    path('employee/add/', EmployeeCreateAPIView.as_view()),
    path('employee/update/<int:emp_id>/', EmployeeUpdateView.as_view()),
    path('employees/', EmployeeListAPIView.as_view()),
    path('employee/destroy/<pk>/', EmployeeDestroyView.as_view()),

    path('create/', PayRollCreateAPIView.as_view()),
    path('item/update/<int:payroll_id>/', PayRollItemUpdateAPIView.as_view()),
    path('all/', PayRollListAPIView.as_view()),
    path('items/', PayRollItemListAPIView.as_view()),
    path('destroy/<pk>/', PayRollDestroyView.as_view()),
    path('item/destroy/<pk>/', PayRollItemDestroyView.as_view()),
]