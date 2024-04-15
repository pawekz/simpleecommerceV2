# Generated by Django 5.0.3 on 2024-04-01 17:16

import django.db.models.deletion
import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('ReviewID', models.IntegerField(primary_key=True, serialize=False)),
                ('ProductID', models.IntegerField()),
                ('CustomerID', models.IntegerField()),
                ('Rating', models.IntegerField()),
                ('ReviewDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('ProductID', models.AutoField(primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=255)),
                ('Description', models.CharField(max_length=255)),
                ('PricePerUnit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('Quantity', models.IntegerField()),
                ('image', models.ImageField(upload_to=products.models.rename_image)),
                ('SellerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.seller')),
            ],
        ),
    ]