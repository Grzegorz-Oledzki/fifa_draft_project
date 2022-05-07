from django.urls import path
from fifa_draft import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups, name='groups'),
    path('group/<str:pk>/', views.group, name='group'),
    path('create-group/', views.create_group, name='create-group'),
    path('create-team/', views.create_team, name='create-team'),
    path('delete-group/<str:pk>/', views.delete_group, name='delete-group'),
    path('team/<str:pk>/', views.team, name='team'),

]

