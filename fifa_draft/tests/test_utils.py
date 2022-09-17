from fifa_draft.tests.test_models import (_create_team_group_and_profile,
                                          _delete_profile_and_group)
from fifa_draft.utils import is_team_name_unique_in_group

profile_data = {
    "username": "grzes test1",
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
group_data2 = {
    "name": "Test group2",
    "number_of_players": 15,
    "draft_order_choice": "Serpentine",
}
team_data2 = {
    "name": "Test team",
    "formation": "4–3–2–1",
}
profile_data2 = {
    "username": "grzes test2",
    "password": "abc"
}


def test_add_team_to_group() -> None:
    team, group, profile = _create_team_group_and_profile(profile_data, group_data, team_data)
    assert team.belongs_group == group
    _delete_profile_and_group(profile, group)


def test_team_max_players_equals_group_max_players() -> None:
    team, group, profile = _create_team_group_and_profile(profile_data, group_data, team_data)
    assert team.max_players == group.number_of_players
    _delete_profile_and_group(profile, group)


def test_profile_in_group_members() -> None:
    team, group, profile = _create_team_group_and_profile(profile_data, group_data, team_data)
    assert profile in group.members.all()
    _delete_profile_and_group(profile, group)


def test_is_name_unique_in_group() -> None:
    team, group, profile = _create_team_group_and_profile(profile_data, group_data, team_data)
    team2, group2, profile2 = _create_team_group_and_profile(profile_data2, group_data2, team_data2)
    assert not is_team_name_unique_in_group(team2.name, group, profile2)
    _delete_profile_and_group(profile, group)
    _delete_profile_and_group(profile2, group2)


