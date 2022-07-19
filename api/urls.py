from django.urls import path
from api import views


urlpatterns = [
    path('', views.get_routes),
    path('teams/', views.get_teams),
    path('team/<str:pk>/', views.get_team),
]