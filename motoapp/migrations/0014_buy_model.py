# Generated by Django 5.0.4 on 2024-05-05 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motoapp', '0013_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='model',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]