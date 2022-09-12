# from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError

from fifa_draft.models import Team
from fifa_draft.utils import is_unique_name
from players.models import Player
from users.models import Profile


def is_team_valid(profile: Profile, team: Team) -> bool:
    unique_name = is_unique_name(team, profile)
    if team.belongs_group.password == team.group_password and profile not in team.belongs_group.members.all() and unique_name:
        return True
    elif team.belongs_group.password != team.group_password:
        raise ValidationError("Incorrect password")
    elif not unique_name:
        raise ValidationError("Name is not unique")
    elif profile in team.belongs_group.members.all():
        raise ValidationError("User have already team in this group")
    else:
        raise ValidationError("Featured image is too big (max 3mb)")


def is_pick_player_valid(player: Player, team, Team, request_profile: Profile):
    pass
