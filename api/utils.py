from typing import List

from api.serializers import PlayerSerializer
from api.validators import validate_if_team_serializer_is_correct, \
    validate_if_pick_player_confirmation_serializer_is_correct
from fifa_draft.models import Group, Team
from fifa_draft.utils import creating_team
from players.models import Player
from players.utils import add_player_to_team_and_group, change_picking_person, pending_player_pick
from users.models import Profile


def group_available_players(group_id: str) -> List[Player]:
    group = Group.objects.get(id=group_id)
    group_players = group.group_players.all()
    available_players = []
    for player in Player.objects.all():
        if player not in group_players:
            available_players.append(player)
    return available_players


def get_profile_and_group(serializer):
    profile = Profile.objects.get(id=serializer["owner"].id)
    group = Group.objects.get(id=serializer["belongs_group"].id)
    return profile, group


def validate_team_and_create_team_if_validated(serializer):
    profile, group = get_profile_and_group(serializer.validated_data)
    validate_if_team_serializer_is_correct(profile, group, serializer.validated_data)
    serializer.save()
    team = Team.objects.get(id=serializer["id"].value)
    creating_team(team, profile)


def get_profile_player_team_and_serializer(player_id, team_id, request):
    profile = Profile.objects.get(user=request.user)
    player = Player.objects.get(sofifa_id=player_id)
    team = Team.objects.get(id=team_id)
    serializer = PlayerSerializer(data=request.data)
    return profile, player, team, serializer


def validate_pick_and_pick_player_if_validated(player, team, profile, serializer):
    validate_if_pick_player_confirmation_serializer_is_correct(player, team, profile, serializer.validated_data)
    add_player_to_team_and_group(team, player)
    next_person = change_picking_person(team, team.owner)
    next_team = team.belongs_group.teams.get(owner=next_person)
    team.belongs_group.picking_person.add(next_person)
    pending_player_pick(next_team, team)
