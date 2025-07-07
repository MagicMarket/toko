from django.shortcuts import render
from .models import TbMenu

# Create your views here.

def landing(request):
    side_menu = TbMenu.objects.filter(is_active=True).order_by('order')  # type: ignore
    # If the path is exactly '/', render dashboard.html, else render landing.html
    if request.path == '/':
        return render(request, 'globalApp/dashboard.html', {'side_menu': side_menu})
    return render(request, 'globalApp/landing.html', {'side_menu': side_menu})

def dashboard(request):
    side_menu = TbMenu.objects.filter(is_active=True).order_by('order')  # type: ignore
    return render(request, 'globalApp/dashboard.html', {'side_menu': side_menu})      