import os
from typing import Tuple

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "draft_fifa.settings")
django.setup()
from django.contrib.auth.models import User

from fifa_draft.models import Group, Team
from fifa_draft.utils import create_team
from users.models import Profile

profile_data = {
    "username": "grzes te11",
    "password": "abc"
}
group_data = {
    "name": "Test group",
    "number_of_players": 15,
    "draft_order_choice": "Serpentine",
}
team_data = {
    "name": "Test team",
    "formation": "4–3–2–1",
}


def _create_user_and_profile(profile_data_dict: dict) -> Profile:
    user = User.objects.create(**profile_data_dict)
    profile = Profile.objects.get(id=user.profile.id)
    return profile


def _create_team_group_and_profile(profile_data_dict: dict, group_data_dict: dict, team_data_dict: dict) -> Tuple[Team, Group, Profile]:
    profile = _create_user_and_profile(profile_data_dict)
    group = Group.objects.create(**group_data_dict, owner=profile)
    team = Team.objects.create(**team_data_dict, owner=profile, belongs_group=group)
    create_team(team, profile)
    return team, group, profile


def _delete_profile_and_group(profile: Profile, group: Group) -> None:
    profile.delete()
    group.delete()


def test_create_group(tmp_path) -> None:
    profile = _create_user_and_profile(profile_data)
    group = Group.objects.create(**group_data, owner=profile)
    assert type(group) == Group
    _delete_profile_and_group(profile, group)


def test_create_team() -> None:
    team, group, profile = _create_team_group_and_profile(profile_data, group_data, team_data)
    assert type(team) == Team
    # _delete_profile_and_group(profile, group)


