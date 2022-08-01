from django.urls import path
from api import views


urlpatterns = [
    path("", views.get_routes),
    path("teams/", views.get_teams),
    path("team/<str:pk>/", views.get_team),
    path("groups/", views.get_groups),
    path("group/<str:pk>/", views.get_group),
    path("player/<str:pk>/", views.get_player),
    path("user/<str:pk>/", views.get_profile),
]
