from django.urls import path
from fifa_draft import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-group/', views.create_group, name='create-group')
]