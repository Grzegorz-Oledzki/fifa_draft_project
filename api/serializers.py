from rest_framework import serializers

from fifa_draft.models import Group, Team
from players.models import Player
from users.models import Profile


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Team
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_teams(self, obj):
        teams = obj.team_set.all()
        serializer = TeamSerializer(teams, many=True)
        return serializer.data
