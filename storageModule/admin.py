from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock', 'price', 'last_update_price', 'product_code')
    search_fields = ('product', 'product_code')
