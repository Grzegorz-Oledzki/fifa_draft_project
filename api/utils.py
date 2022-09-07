from typing import List

from fifa_draft.models import Group, Team
from fifa_draft.utils import is_unique_name
from players.models import Player
from users.models import Profile


def is_team_valid(team: Team, profile: Profile, belongs_group: Group) -> bool:
    unique_name = is_unique_name(team, profile)
    return (
        belongs_group.password == team.group_password
        and profile not in belongs_group.members.all()
        and unique_name
    )


def group_available_players(group_id) -> List[Player]:
    group = Group.objects.get(id=group_id)
    group_players = group.group_players.all()
    available_players = []
    for player in Player.objects.all():
        if player not in group_players:
            available_players.append(player)
    return available_players
