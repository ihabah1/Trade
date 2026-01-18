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
# Seed Catalog (Lobby)
# -------------------------------
class LobbyView(LoginRequiredMixin, TemplateView):
    template_name = "app/lobby.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Plants / Seeds only (10 products)
        context["seeds"] = [
    {"name": "Basil Seeds", "price": "2.20", "image": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449"},
    {"name": "Tomato Seeds", "price": "3.50", "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea"},
    {"name": "Carrot Seeds", "price": "2.90", "image": "https://www.allthatgrows.in/cdn/shop/products/Carrot-Orange.jpg?v=1598079671"},
    {"name": "Lettuce Seeds", "price": "2.10", "image": "https://www.100daysofrealfood.com/wp-content/uploads/2023/11/vecteezy_lettuce-salad-leaf-isolated-on-white-background-with_5582269-1200x800.jpg"},
    {"name": "Pepper Seeds", "price": "3.10", "image": "https://sc02.alicdn.com/kf/H908de00a859846ffb6e84761ad68a831R.png"},
    {"name": "Cucumber Seeds", "price": "2.80", "image": "https://www.seedsnow.com/cdn/shop/products/Cucumber_-_Ashley_seeds.jpg?v=1681331732&width=1214"},
    {"name": "Spinach Seeds", "price": "1.90", "image": "https://cdn.britannica.com/30/82530-050-79911DD4/Spinach-leaves-vitamins-source-person.jpg?w=300"},
    {"name": "Parsley Seeds", "price": "1.80", "image": "https://sc02.alicdn.com/kf/Hf89de3d8dc7e4d7a9350c1b1f74ca154Z.png"},
    {"name": "Mint Seeds", "price": "2.00", "image": "https://www.kenshodaily.com/cdn/shop/products/MintLeaves_720x@2x.png?v=1672742949"},
    {"name": "Onion Seeds", "price": "2.60", "image": "https://produits.bienmanger.com/36700-0w0h0_Organic_Red_Onion_From_Italy.jpg"},
]

        return context


# -------------------------------
# Basket (Test Only)
# -------------------------------
from django.contrib import messages

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
# Submit Score (Legacy POST)
# -------------------------------
@login_required
def submit_score(request):
    if request.method == "POST":
        game_name = request.POST.get("game_name")
        score = int(request.POST.get("score", 0))
        game, _ = Game.objects.get_or_create(name=game_name)
        GameScore.objects.create(user=request.user, game=game, score=score)
        messages.success(request, "Your score has been saved!")
        return redirect('app:profile')
    return redirect('app:lobby')


# -------------------------------
# Game Views
# -------------------------------
@login_required
def play_ping_pong(request):
    return render(request, 'games/ping_pong.html')


@login_required
def play_tetris(request):
    return render(request, 'games/tetris.html')


# -------------------------------
# API Endpoint: Update Points
# -------------------------------
@login_required
def update_points(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            points = int(data.get("points", 0))
            user = request.user

            game, _ = Game.objects.get_or_create(
                name="Ping Pong",
                defaults={"max_score": 3}
            )

            GameScore.objects.create(user=user, game=game, score=points)

            total = GameScore.objects.filter(user=user).aggregate(Sum('score'))['score__sum'] or 0
            return JsonResponse({"success": True, "total_score": total})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


# -------------------------------
# Signup Redirect (Disable Registration)
# -------------------------------
def redirect_signup_to_login(request):
    return redirect('/accounts/login/')


# -------------------------------
# Home Page
# -------------------------------
class HomeView(View):
    def get(self, request):
        return render(request, 'app/index.html')
