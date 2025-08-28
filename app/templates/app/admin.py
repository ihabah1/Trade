from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'seller', 'created_at')
    search_fields = ('name', 'seller__username')
