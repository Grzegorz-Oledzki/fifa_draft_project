from urllib.request import Request

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (GroupSerializer, PlayerSerializer,
                             ProfileSerializer, TeamSerializer, GroupAvailablePlayersSerializer)
from api.utils import is_team_valid, group_available_players
from fifa_draft.models import Group, Team
from players.models import Player
from users.models import Profile


@api_view(["GET", "POST"])
def get_routes(request: Request) -> Response:

    routes = [
        {"GET": "/api/groups"},
        {"GET": "/api/group/id"},
        {"GET": "/api/team/id"},
        {"GET": "/api/players/choose-team"},
        {"GET": "/api/players/players-pick/id"},
        {"POST": "/api/players/pending-player-pick-confirmation/sofifa_id/id"},
        {"POST": "/api/players/player-pick-confirmation/sofifa_id/id"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]

    return Response(routes)


@api_view(["GET"])
def get_teams(request: Request) -> Response:
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_team(request: Request, pk: str) -> Response:
    team = Team.objects.get(id=pk)
    serializer = TeamSerializer(team, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_profile(request: Request, pk: str) -> Response:
    profile = Profile.objects.get(id=pk)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def create_team(request: Request) -> Response:
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        team_password = serializer.validated_data["group_password"]
        profile = serializer.validated_data["owner"]
        belongs_group = serializer.validated_data["belongs_group"]
        if is_team_valid(team_password, profile, belongs_group):
            serializer.save()
            belongs_group.members.add(profile)
            team = Team.objects.get(id=serializer["id"].value)
            profile.draft_teams.add(team)
            belongs_group.teams.add(team)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
# need to add specific validation messages


@api_view(["GET"])
def get_groups(request: Request) -> Response:
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_group(request: Request, pk: str) -> Response:
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer(group, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def create_group(request: Request) -> Response:
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["GET"])
def get_player(request: Request, pk: str) -> Response:
    player = Player.objects.get(id=pk)
    serializer = PlayerSerializer(player, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_group_available_players(request: Request, pk: str) -> Response:
    players = group_available_players(pk)
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)
