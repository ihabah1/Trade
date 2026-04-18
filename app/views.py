import json

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.conf import settings

from .models import GameScore, Game
from .economics import calculate_final_score
from .services.data_service import build_lobby_data


# -------------------------------
# Home
# -------------------------------
class HomeView(View):
    def get(self, request):
        return render(request, 'app/index.html')


# -------------------------------
# Lobby (FAST load - no data here)
# -------------------------------
class LobbyView(LoginRequiredMixin, TemplateView):
    template_name = "app/lobby.html"


# -------------------------------
# 🚀 API - loads data async
# -------------------------------
def lobby_data_api(request):
    data = build_lobby_data()
    return JsonResponse(data)


# -------------------------------
# Economic Index
# -------------------------------
class EconomicIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'app/economic_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trend'] = '⬆ Positive Trend'
        context['score'] = 'Weighted Score: 68%'
        context['data'] = [0.42, 0.10, 0.15, 0.05]
        return context


@login_required
def economic_index_api(request):
    api_key = settings.OPENROUTER_API_KEY
    data = calculate_final_score(api_key)
    return JsonResponse(data)


# -------------------------------
# User Dashboard
# -------------------------------
@login_required
def user_dashboard(request):
    game_scores = GameScore.objects.filter(user=request.user).order_by('-played_at')
    total_points = game_scores.aggregate(Sum('score'))['score__sum'] or 0
    return render(request, 'app/profile.html', {
        'game_scores': game_scores,
        'total_points': total_points
    })


# -------------------------------
# Basket
# -------------------------------
def basket(request):
    seed_name = request.GET.get("name")
    seed_price = request.GET.get("price")

    if request.method == "POST":
        messages.success(request, "🚚 The product is on the way!")
        return redirect(request.path + f"?name={seed_name}&price={seed_price}")

    return render(request, "app/basket.html", {
        "seed_name": seed_name,
        "seed_price": seed_price,
    })


# -------------------------------
# Games
# -------------------------------
@login_required
def play_ping_pong(request):
    return render(request, 'games/ping_pong.html')


@login_required
def play_tetris(request):
    return render(request, 'games/tetris.html')