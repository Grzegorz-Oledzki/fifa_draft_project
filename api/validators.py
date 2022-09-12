from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from api.utils import is_unique_name_api
from fifa_draft.models import Group
from users.models import Profile


def team_validation_errors(
    profile: Profile, group: Group, validated_data: dict
) -> None:
    unique_name = is_unique_name_api(validated_data["group_password"], group, profile)
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
