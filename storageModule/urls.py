from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_landing, name='product-landing'),
    path('image_base64/<int:product_id>/', views.product_image_base64, name='product-image-base64'),
] 