from typing import List

from fifa_draft.models import Group, Team
from players.models import Player
from users.models import Profile


def is_unique_name_api(team_name: str, group: Group, profile) -> bool:
    for team_in_group in group.teams.all():
        if (
            str(team_in_group).lower() == str(team_name).lower()
            and profile != team_in_group.owner
        ):
            return False
    return True


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
