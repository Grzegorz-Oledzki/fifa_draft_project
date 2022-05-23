from import_export import resources
from fifa_draft.models import Player


class PlayerResource(resources.ModelResource):
    class meta:
        model = Player
