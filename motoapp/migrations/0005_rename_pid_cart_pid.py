# Generated by Django 5.0.4 on 2024-04-17 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motoapp', '0004_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='Pid',
            new_name='pid',
        ),
    ]