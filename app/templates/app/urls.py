# app/urls.py
from django.urls import path
from .views import home, LobbyView, create_room, join_room  # import your view callables

urlpatterns = [
    path('', home, name='index'),
    path('lobby/', LobbyView.as_view(), name='lobby'),

]
