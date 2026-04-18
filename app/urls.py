from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("profile/", views.user_dashboard, name="profile"),
    path("play/ping-pong/", views.play_ping_pong, name="play_ping_pong"),
    path("play/tetris/", views.play_tetris, name="play_tetris"),
    path("economic-index/", views.EconomicIndexView.as_view(), name="economic_index"),
    path("basket/", views.basket, name="basket"),

    # Lobby
    path("lobby/", views.LobbyView.as_view(), name="lobby"),

    # 🔥 API
    path("api/lobby-data/", views.lobby_data_api, name="lobby_data_api"),
]