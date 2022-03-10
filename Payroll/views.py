from django.contrib.auth.models import User
from rest_framework import status
from .models import Team
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import (
    AddTeamSerializer,
    RetriveTeamSerializer
)
from utils.pagination import LimitOffsetPagination

# Create your views here.
class AddTeamView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AddTeamSerializer
    def post(self, request, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        if data.get('company_id'):
            print(user.is_staff, "    ", user.is_authenticated, "    ", user.is_superuser)
            if user.is_superuser:
                user = User.objects.get(pk=int(data.get('company_id')))
        if data.get("team_name"):
            print("hahahaha")
            if Team.objects.filter(user=self.request.user.id).filter(team_name=data.get("team_name")).exists():
                return Response({"messgae": "Team name must be unique"}, status=status.HTTP_205_RESET_CONTENT)
            Team.objects.create(
                user = user,
                team_name = data.get("team_name"),
                address = data.get("address"),
                postcode = data.get("postcode"),
                province = data.get("province"),
                country = data.get("country"),
                note = data.get("note")
                )
            return Response({'success': "Team added to list"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_205_RESET_CONTENT)



class UpdateTeamView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddTeamSerializer
    def update(self, request, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        if data.get('company_id'):
            if user.is_superuser:
                user = User.objects.get(pk=int(data.get('company_id')))

        if data.get("team_name") and data.get("team_id"):
            if Team.objects.filter(user=user.id).filter(team_name=data.get("team_name")).exists():
                current_team = Team.objects.filter(user=user.id).filter(team_name=data.get("team_name"))
                if current_team.first().id == data.get("team_id"):
                    pass
                else:
                    return Response({"messgae": "Team name must be unique"}, status=status.HTTP_205_RESET_CONTENT)

            team = Team.objects.get(user=self.request.user.id, pk=int(data.get("team_id")))

            team.team_name = data.get("team_name")
            team.address = data.get("address")
            team.postcode = data.get("postcode")
            team.province = data.get("province")
            team.country = data.get("country")
            team.note = data.get("note")

            team.save()
            return Response({'success': "Team {} updated".format(team.team_name)}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_205_RESET_CONTENT)


'''

'''
class TeamListView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RetriveTeamSerializer
    def get_queryset(self):
        return Team.objects.filter(user=self.request.user)


class TeamDestroyView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    permission_class = (permissions.IsAuthenticated,)
    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            if not Team.objects.filter(user=self.request.user.id, pk=instance.id).exists():
                return Response({"message": "you are an unauthorized user to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                super().perform_destroy(instance)
        else:
            super().perform_destroy(instance)