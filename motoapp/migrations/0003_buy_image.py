# Generated by Django 5.0.4 on 2024-04-15 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motoapp', '0002_bcategory_buy'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_images/'),
        ),
    ]
