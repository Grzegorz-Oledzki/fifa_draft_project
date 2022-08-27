from import_export import resources

from players.models import Player


class PlayerResource(resources.ModelResource):
    class meta:
        model = Player
