from typing import List

from api.validators import validate_if_team_serializer_is_correct
from fifa_draft.models import Group, Team
from fifa_draft.utils import creating_team
from players.models import Player
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
