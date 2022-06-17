# Generated by Django 4.0.4 on 2022-06-17 09:41

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_user_alter_order_user_alter_productinbasket_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, max_length=48, region=None, unique=True),
        ),
    ]
