from re import T
from django.db import models

# Create your models here.

class Product(models.Model):
    product = models.CharField(max_length=255)
    stock = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_update_price = models.DateField(auto_now=True)
    product_code = models.CharField(max_length=100, unique=True,)
    deleted = models.BooleanField(null=True)
    # Instead of ImageField, store the static path as a CharField
    image = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Relative path to image in toko/globalApp/static/product_photo/"
    )

    def __str__(self):
        return f"{self.product} ({self.product_code})"

class TbProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    last_update_price = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.price} at {self.updated_at}"
