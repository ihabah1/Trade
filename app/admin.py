from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import GameScore, Game


# -------------------------------
# Home Page
# -------------------------------
class HomeView(View):
    def get(self, request):
        return render(request, 'app/index.html')


# -------------------------------
# Game Lobby (Choose a Game)
# -------------------------------
@method_decorator(login_required, name='dispatch')
class LobbyView(View):
    def get(self, request):
        games = Game.objects.all()
        return render(request, 'app/lobby.html', {'games': games})


# -------------------------------
# User Profile (Points Dashboard)
# -------------------------------
@login_required
def user_profile(request):
    total_points = GameScore.total_score_for_user(request.user)
    recent_scores = (
        GameScore.objects
                 .filter(user=request.user)
                 .order_by('-played_at')[:5]
    )
    return render(request, 'account/profile.html', {
        'total_points': total_points,
        'game_scores': recent_scores,
    })


# -------------------------------
# Save Score (POST)
# -------------------------------
@login_required
def submit_score(request):
    if request.method == 'POST':
        game_name = request.POST.get('game_name', '')
        try:
            score = int(request.POST.get('score', 0))
        except ValueError:
            score = 0
        GameScore.objects.create(user=request.user, game_name=game_name, score=score)
        return redirect('profile')
    return redirect('lobby')


# -------------------------------
# Play Ping‑Pong
# -------------------------------
@login_required
def play_ping_pong(request):
    return render(request, 'games/ping_pong.html')


# -------------------------------
# Play Tetris
# -------------------------------
@login_required
def play_tetris(request):
    return render(request, 'games/tetris.html')
