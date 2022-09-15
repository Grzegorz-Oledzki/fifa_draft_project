from collections import OrderedDict

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from fifa_draft.models import Group, Team
from fifa_draft.utils import is_team_name_unique_in_group
from players.models import Player
from users.models import Profile


def validate_if_team_serializer_is_correct(
    profile: Profile, group: Group, validated_data: OrderedDict
) -> None:
    unique_name = is_team_name_unique_in_group(validated_data["name"], group, profile)
    if group.password != validated_data["group_password"]:
        raise ValidationError(_("Incorrect password"), code="invalid password")
    elif not unique_name:
        raise ValidationError(_("Name is not unique"), code="invalid name")
    elif profile in group.members.all():
        raise ValidationError(
            _("User have already team in this group"), code="invalid user"
        )
    elif validated_data["featured_image"]:
        if validated_data["featured_image"].size > (3 * 1024 * 1024):
            raise ValidationError(
                _("Featured image is too big (max 3mb)"), code="invalid image"
            )


def validate_if_profile_is_picking_person(profile: Profile, team: Team):
    if profile not in team.belongs_group.picking_person.all():
        raise ValidationError(
            _("User is not picking person"),
            code="request profile is not picking person",
        )


def validate_if_pick_player_serializer_is_correct(
    player: Player, team: Team, profile: Profile, serializer: OrderedDict
) -> None:
    if serializer["sofifa_id"] != player.sofifa_id:
        raise ValidationError(
            _("Wrong player was picked"),
            code="wrong player (url player_id vs sofifa_id",
        )
    elif player in team.belongs_group.group_players.all():
        raise ValidationError(
            _("Player is not available"), code="player was picked earlier"
        )
    elif profile != team.owner:
        raise ValidationError(
            _("Request profile is not team owner"), code="request profile error"
        )
