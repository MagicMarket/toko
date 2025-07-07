from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('', views.landing, name='globalapp-landing'),
    path('dashboard/', views.dashboard, name='globalapp-dashboard'),
] 

def landing(request):
    return HttpResponse(b"<h1>Welcome to the Global App Landing Page</h1>") 