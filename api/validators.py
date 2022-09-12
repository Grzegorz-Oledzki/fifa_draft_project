from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from fifa_draft.models import Team
from fifa_draft.utils import is_unique_name
from users.models import Profile


def team_validation_errors(profile: Profile, team: Team) -> None:
    unique_name = is_unique_name(team, profile)
    if team.belongs_group.password != team.group_password:
        raise ValidationError(_("Incorrect password"), code='invalid password')
    elif not unique_name:
        raise ValidationError(_("Name is not unique"), code='invalid name')
    elif profile in team.belongs_group.members.all():
        raise ValidationError(_("User have already team in this group"), code='invalid user')
    else:
        raise ValidationError(_("Featured image is too big (max 3mb)"), code='invalid image')

