from django.urls import path

from api import views

urlpatterns = [
    path("", views.get_routes),
    path("teams/", views.get_teams),
    path("team/<str:pk>/", views.get_team),
    path("create_team/", views.create_team),
    path("all_groups/", views.get_groups),
    path("group/<str:pk>/", views.get_group),
    path("create_group/", views.create_group),
    path("player/<str:pk>/", views.get_player),
    path("group_players/<str:pk>/", views.get_group_available_players),
    path("user/<str:pk>/", views.get_profile),
]
