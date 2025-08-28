# sellitnow/urls.py
from django.contrib import admin
from django.urls import path, include

from app.views import (
    LobbyView,
    play_ping_pong,
    play_tetris,
    submit_score,
    update_points,
    redirect_signup_to_login
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('app.urls')),

    path('lobby/', LobbyView.as_view(), name='lobby'),
    path('play/ping-pong/', play_ping_pong, name='play_ping_pong'),
    path('play/tetris/', play_tetris, name='play_tetris'),
    path('submit-score/', submit_score, name='submit_score'),
    path('api/update-points/', update_points, name='update_points'),

    # **Put signup redirect BEFORE allauth URLs**
    path('accounts/signup/', redirect_signup_to_login, name='account_signup'),

    path('accounts/', include('allauth.urls')),
]

