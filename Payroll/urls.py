from django.urls import path
from .views import (
    AddTeamView,
    TeamListView,
    UpdateTeamView,
    TeamDestroyView
)


urlpatterns = [
    path('add/', AddTeamView.as_view()),
    path('teams/', TeamListView.as_view()),
    path('team/update/', UpdateTeamView.as_view()),
    path('team/destroy/<pk>/', TeamDestroyView.as_view())
]