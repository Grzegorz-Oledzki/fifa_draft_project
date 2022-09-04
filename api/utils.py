from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from requests import Response

from fifa_draft.utils import creating_team, is_unique_name
from users.models import Profile


def team_form_validation_api(team_password, profile: Profile, belongs_group) -> bool:
    unique_name = is_unique_name
    return (
        belongs_group.password == team_password
        and profile not in belongs_group.members.all()
        and unique_name
    )
