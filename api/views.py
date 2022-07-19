from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import TeamSerializer
from fifa_draft.models import Team, Group


@api_view(['GET', 'POST'])
def get_routes(request):

    routes = [
        {'GET': '/api/groups'},
        {'GET': '/api/group/id'},
        {'GET': '/api/team/id'},
        {'GET': '/api/players/choose-team'},
        {'GET': '/api/players/players-pick/id'},
        {'POST': '/api/players/pending-player-pick-confirmation/sofifa_id/id'},
        {'POST': '/api/players/player-pick-confirmation/sofifa_id/id'},
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},

    ]

    return Response(routes)


@api_view(["GET"])
def get_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_team(request, pk):
    team = Team.objects.get(id=pk)
    serializer = TeamSerializer(team, many=False)
    return Response(serializer.data)
