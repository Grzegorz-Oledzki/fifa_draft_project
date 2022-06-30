from django.urls import path
from players import views

urlpatterns = [
    path("upload/", views.upload_players),
    path("players/", views.players, name="players"),
    path("choose-team/", views.choose_team, name="choose-team"),
    path("players-pick/<str:pk>/", views.players_pick, name="players-pick"),
    path(
        "player-pick-confirmation/<str:pk>/<str:team_id>/",
        views.player_pick_confirmation,
        name="player-pick-confirmation",
    )]