from rest_framework import serializers
from fifa_draft.models import Team, Group
from players.models import Player
from users.models import Profile


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
