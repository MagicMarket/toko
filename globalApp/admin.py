from django.contrib import admin
from .models import TbMenu

@admin.register(TbMenu)
class TbMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon', 'order', 'is_active', 'parent')
    search_fields = ('name', 'url', 'icon')
    list_filter = ('is_active',)
