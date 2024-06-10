# Generated by Django 5.0.4 on 2024-04-12 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('modelv', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('fuel', models.CharField(choices=[('none', 'Select Fuel type'), ('cng_hybrid', 'CNG and Hybrid'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('lpg', 'LPG'), ('petrol', 'Petrol')], default='none', max_length=20)),
                ('km_driven', models.CharField(blank=True, max_length=50, null=True)),
                ('no_owners', models.CharField(choices=[('none', 'Select No.of Owners'), ('first', '1st'), ('second', '2nd'), ('third', '3rd'), ('fourth_plus', '4+')], default='none', max_length=20)),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicle_images/')),
                ('pname', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='motoapp.category')),
            ],
        ),
    ]
