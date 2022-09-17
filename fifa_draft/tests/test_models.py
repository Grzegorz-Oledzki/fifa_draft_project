import os
from typing import Tuple

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "draft_fifa.settings")
django.setup()
from fifa_draft.models import Group, Team
from django.contrib.auth.models import User
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


def _create_user_and_profile() -> Profile:
    user = User.objects.create(**profile_data)
    profile = Profile.objects.get(id=user.profile.id)
    return profile


def _create_team_group_and_profile() -> Tuple[Team, Group, Profile]:
    profile = _create_user_and_profile()
    group = Group.objects.create(**group_data, owner=profile)
    team = Team.objects.create(**team_data, owner=profile, belongs_group=group)
    return team, group, profile


def _delete_profile_and_group(profile: Profile, group: Group) -> None:
    profile.delete()
    group.delete()


def test_create_group(tmp_path) -> None:
    profile = _create_user_and_profile()
    group = Group.objects.create(**group_data, owner=profile)
    assert type(group) == Group
    _delete_profile_and_group(profile, group)


def test_create_team() -> None:
    team, group, profile = _create_team_group_and_profile()
    assert type(team) == Team
    _delete_profile_and_group(profile, group)


def test_add_team_to_group() -> None:
    team, group, profile = _create_team_group_and_profile()
    assert team.belongs_group == group
    _delete_profile_and_group(profile, group)
