from urllib.request import Request

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (GroupSerializer, PlayerSerializer,
                             ProfileSerializer, TeamSerializer)
from api.utils import group_available_players, get_profile_and_team
from api.validators import is_team_valid, is_pick_player_valid
from fifa_draft.models import Group, Team
from fifa_draft.utils import creating_team
from players.models import Player
from players.utils import add_player_to_team_and_group, change_picking_person, pending_player_pick
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
        serializer.save()
        profile, team = get_profile_and_team(serializer)
        if is_team_valid(profile, team):
            creating_team(team, profile)
            return Response(serializer.data)
        else:
            team.delete()
            return Response(serializer.errors, status=400)
    return Response(serializer.errors, status=400)


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
def get_group_available_players(request: Request, group_id: str) -> Response:
    players = group_available_players(group_id)
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def pick_player_confirmation(request: Request, player_id: str, team_id: str) -> Response:
    player = Player.objects.get(sofifa_id=player_id)
    team = Team.objects.get(id=team_id)
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        if is_pick_player_valid(player, team):
            add_player_to_team_and_group(team, player)
            next_person = change_picking_person(team, team.owner)
            next_team = team.belongs_group.teams.get(owner=next_person)
            team.belongs_group.picking_person.add(next_person)
            pending_player_pick(next_team, team)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def pending_player_confirmation(request: Request, player_id: str, team_id: str) -> Response:
    player = Player.objects.get(sofifa_id=player_id)
    team = Team.objects.get(id=team_id)
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        if player not in team.belongs_group.group_players.all() and serializer.validated_data["sofifa_id"] == int(player_id):
            team.pending_player.add(player)
            return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def delete_pending_player_confirmation(request: Request, player_id: str, team_id: str) -> Response:
    player = Player.objects.get(sofifa_id=player_id)
    team = Team.objects.get(id=team_id)
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data["sofifa_id"] == int(player_id):
            team.pending_player.remove(player)
            return Response(serializer.data)
    return Response(serializer.errors, status=400)





