from urllib.request import Request

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (GroupSerializer, PlayerSerializer,
                             ProfileSerializer, TeamSerializer)
from api.utils import (get_profile_player_team_and_serializer,
                       group_available_players,
                       validate_pick_and_pick_player_if_validated,
                       validate_team_and_create_team_if_validated,
                       validate_pending_pick_and_pick_player_if_validated)
from fifa_draft.models import Group, Team
from players.models import Player
from users.models import Profile


@api_view(["GET", "POST"])
def get_routes(request: Request) -> Response:

    routes = [
        {"GET": "/api/all-groups"},
        {"GET": "/api/group/id"},
        {"GET": "/api/team/id"},
        {"GET": "/api/teams/"},
        {"GET": "/api/player/id"},
        {"GET": "/api/group_players/group_id"},

        {"POST": "/api/create-team"},
        {"POST": "/api/create-group"},

        {"POST": "/api/player-pick-confirmation/player_id/team_id"},
        {"POST": "/api/pending-player-pick-confirmation/player_id/team_id"},
        {"POST": "/api/delete-pending-player-pick-confirmation/player_id/team_id"},

        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]

    return Response(routes)


@api_view(["GET"])
def current_user(request) -> Response:
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


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
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    validate_team_and_create_team_if_validated(serializer)
    return Response(serializer.data)


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
    player = Player.objects.get(sofifa_id=pk)
    serializer = PlayerSerializer(player, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_group_available_players(request: Request, group_id: str) -> Response:
    players = group_available_players(group_id)
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def pick_player_confirmation(
    request: Request, player_id: str, team_id: str
) -> Response:
    profile, player, team, serializer = get_profile_player_team_and_serializer(
        player_id, team_id, request
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    validate_pick_and_pick_player_if_validated(player, team, profile, serializer)
    return Response(serializer.data)


@api_view(["POST"])
def pending_player_confirmation(
    request: Request, player_id: str, team_id: str
) -> Response:
    profile, player, team, serializer = get_profile_player_team_and_serializer(
        player_id, team_id, request
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    validate_pending_pick_and_pick_player_if_validated(player, team, profile, serializer)
    team.pending_player.add(player)
    return Response(serializer.data)


@api_view(["POST"])
def delete_pending_player_confirmation(
    request: Request, player_id: str, team_id: str
) -> Response:
    profile, player, team, serializer = get_profile_player_team_and_serializer(
        player_id, team_id, request)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    validate_pending_pick_and_pick_player_if_validated(player, team, profile, serializer)
    team.pending_player.remove(player)
    return Response(serializer.data)
