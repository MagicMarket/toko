# Generated by Django 5.2.4 on 2025-07-07 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storageModule', '0008_alter_product_last_update_price_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='last_update_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
