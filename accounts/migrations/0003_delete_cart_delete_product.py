# Generated by Django 5.0.3 on 2024-04-02 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_product_cart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
