from django.urls import path
from fifa_draft import views
urlpatterns = [
    path('', views.home),
]