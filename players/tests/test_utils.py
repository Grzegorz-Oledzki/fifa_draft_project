from fifa_draft.tests.test_models import _create_team_group_and_profile, _delete_profile_and_group
from players.tests.test_model import _create_player
from players.utils import add_player_to_team_and_group

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


def test_adding_player_to_team_and_group() -> None:
    team, group, profile = _create_team_group_and_profile(profile_data, group_data, team_data)
    group.picking_history = "Draft started!:"
    player = _create_player()
    add_player_to_team_and_group(team, player)
    assert player in team.team_players.all()
    _delete_profile_and_group(profile, group)
    player.delete()
