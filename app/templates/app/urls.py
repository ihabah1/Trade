# app/urls.py
from django.urls import path
from .views import home, LobbyView, create_room, join_room  # import your view callables

from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    urlpatterns = [
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
