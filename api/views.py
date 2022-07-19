from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
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