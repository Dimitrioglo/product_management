# Generated by Django 3.2.7 on 2021-09-29 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlists', '0002_rename_publications_wishlist_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='description',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='price',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='sku',
        ),
    ]