import os

import django
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "draft_fifa.settings")
django.setup()

from fifa_draft.models import Group, Team
from users.models import Profile

profile_data = {
    "name": "Grzesiu Test",
    "username": "grzes test",
}

profile_data2 = {
    "name": "Grzesiu Test 2",
    "username": "grzes test 2",
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
team_data2 = {
    "name": "Test team",
    "formation": "4–3–3",
}


class TestPlayerUtils(TestCase):
    def setUp(self) -> None:
        self._create_profiles_group_and_team_and_connect_them()

    def test_get_profile(self) -> None:
        self.assertEqual(type(self.profile), Profile)

    def test_get_group_name_and_owner(self) -> None:
        self.assertEqual(self.group.name, group_data["name"])
        self.assertEqual(self.group.owner, self.profile)

    def test_get_team_name_and_owner(self) -> None:
        self.assertEqual(self.team.name, team_data["name"])
        self.assertEqual(self.team.owner, self.profile)

    def test_if_team_is_in_group(self) -> None:
        self.assertEqual(self.team.belongs_group, self.group)

    def test_add_second_team_to_group(self) -> None:
        self.team2 = Team.objects.create(
            **team_data2, owner=self.profile2, belongs_group=self.group
        )
        self.assertEqual(self.team2.belongs_group, self.group)
        self.assertEqual(self.team2.owner, self.profile2)

    def _create_profiles_group_and_team_and_connect_them(self):
        self.profile = Profile.objects.create(**profile_data)
        self.profile2 = Profile.objects.create(**profile_data2)
        self.group = Group.objects.create(**group_data, owner=self.profile)
        self.group.members.add(self.profile)
        self.team = Team.objects.create(
            **team_data, owner=self.profile, belongs_group=self.group
        )
