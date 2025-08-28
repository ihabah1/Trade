from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# 🎮 Track each game
# in models.py
class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    max_score = models.IntegerField(default=3)

class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # ← this field
    score = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

# 🛍️ Product listing (e.g., shop or marketplace)
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name

# 👤 Extended user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"
