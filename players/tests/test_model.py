from django.test import TestCase
from players.models import Player

data = {
    "id": 127,
    "sofifa_id": 111111,
    "player_url": "",
    "short_name": "G. Olędzki",
    "player_positions": "CF, ST",
    "overall": 69,
    "age": 27,
    "height_cm": 184,
    "weight_kg": 96,
    "club_name": "FC Katowice",
    "preferred_foot": "Left",
    "weak_foot": 2,
    "skill_moves": 2,
    "work_rate": "Medium/Medium",
    "pace": 70,
    "shooting": 72,
    "passing": 67,
    "dribbling": 68,
    "defending": 64,
    "physic": 80,
    "player_face_url": "",
    "club_logo_url": "",
    "nation_flag_url": "https://cdn.sofifa.net/flags/pl.png"
}


def _create_player() -> Player:
    player = Player.objects.create(**data)
    return player


class TestPlayer(TestCase):
    def test_get_player_by_na(self) -> None:
        player = Player.objects.create(**data)
        self.assertEqual(player.short_name, data['short_name'])

    def test_get_player_by_sofifa_id(self) -> None:
        player = Player.objects.create(**data)
        self.assertEqual(player.sofifa_id, data['sofifa_id'])
