from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # כל האפליקציה נטענת מפה
    path('', include('app.urls')),

    # allauth
    path('accounts/', include('allauth.urls')),
]