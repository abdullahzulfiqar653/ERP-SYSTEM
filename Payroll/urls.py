from django.urls import path
from .views import (
    AddTeamView,
    TeamListView,
    TeamFormListView,
    UpdateTeamView,
    TeamsDeleteAPIView,
    TeamRetrieveAPIView,

    EmployeeUpdateView,
    EmployeeCreateAPIView,
    EmployeeRetrieveAPIView,
    EmployeeListAPIView,
    EmployeesDeleteAPIView,

    PayRollCreateAPIView,
    PayRollListAPIView,
    PayRollRetrieveAPIView,
    PayRollsDeleteAPIView,
    PayRollItemDestroyView,
    PayRollItemUpdateAPIView,
)


urlpatterns = [
    path('team/add/', AddTeamView.as_view()),
    path('teams/', TeamListView.as_view()),
    path('list/teams/', TeamFormListView.as_view()),
    path('team/<pk>/', TeamRetrieveAPIView.as_view()),
    path('team/update/<int:team_id>/', UpdateTeamView.as_view()),
    path('teams/destroy/', TeamsDeleteAPIView.as_view()),

    path('employee/add/', EmployeeCreateAPIView.as_view()),
    path('employee/update/<int:emp_id>/', EmployeeUpdateView.as_view()),
    path('employee/<pk>/', EmployeeRetrieveAPIView.as_view()),
    path('employees/', EmployeeListAPIView.as_view()),
    path('employees/destroy/', EmployeesDeleteAPIView.as_view()),

    path('create/', PayRollCreateAPIView.as_view()),
    path('items/update/<int:payroll_id>/', PayRollItemUpdateAPIView.as_view()),
    path('all/', PayRollListAPIView.as_view()),
    path('items/<pk>/', PayRollRetrieveAPIView.as_view()),
    path('destroy/', PayRollsDeleteAPIView.as_view()),
    path('item/destroy/<pk>/', PayRollItemDestroyView.as_view()),

]
