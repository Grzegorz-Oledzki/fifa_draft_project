from django.urls import path
from fifa_draft import views

urlpatterns = [
    path("", views.home, name="home"),
    path("groups/", views.groups, name="groups"),
    path("group/<str:pk>/", views.group, name="group"),
    path("create-group/", views.create_group, name="create-group"),
    path("edit-group/<str:pk>/", views.edit_group, name="edit-group"),
    path("create-team/", views.create_team, name="create-team"),
    path("edit-team/<str:pk>/", views.edit_team, name="edit-team"),
    path("delete-group/<str:pk>/", views.delete_group, name="delete-group"),
    path("team/<str:pk>/", views.team, name="team"),
    path('upload/', views.upload_players),
    path('players/', views.players, name="players"),
]
