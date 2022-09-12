from typing import List

from fifa_draft.models import Group, Team
from fifa_draft.utils import is_unique_name
from players.models import Player
from users.models import Profile


def is_team_serializer_valid(profile: Profile, team: Team) -> bool:
    unique_name = is_unique_name(team, profile)
    return (
        team.belongs_group.password == team.group_password
        and profile not in team.belongs_group.members.all()
        and unique_name)


def group_available_players(group_id: str) -> List[Player]:
    group = Group.objects.get(id=group_id)
    group_players = group.group_players.all()
    available_players = []
    for player in Player.objects.all():
        if player not in group_players:
            available_players.append(player)
    return available_players


def get_profile_and_team(serializer):
    profile = Profile.objects.get(id=serializer["owner"].value)
    team = Team.objects.get(id=serializer["id"].value)
    return profile, team
