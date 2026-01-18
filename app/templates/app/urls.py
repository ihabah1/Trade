# app/urls.py
from django.urls import path
from .views import home, LobbyView, create_room, join_room  # import your view callables

from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("lobby/", views.LobbyView.as_view(), name="lobby"),
    path("basket/", views.basket, name="basket"),
]


