from django.urls import path
from .views import (
    HomeView, LobbyView, user_dashboard,
    play_ping_pong, play_tetris,
    economic_index_api, EconomicIndexView
)

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('lobby/', LobbyView.as_view(), name='lobby'),
    path('profile/', user_dashboard, name='profile'),
    path('play/ping-pong/', play_ping_pong, name='play_ping_pong'),
    path('play/tetris/', play_tetris, name='play_tetris'),
    path('economic-index/', EconomicIndexView.as_view(), name='economic_index'),
    path('economic-index/api/', economic_index_api, name='economic_index_api')

]