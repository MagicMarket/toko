from django.db import models

# Create your models here.

class TbMenu(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
