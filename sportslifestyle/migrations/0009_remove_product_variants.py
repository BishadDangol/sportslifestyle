# Generated by Django 4.1.5 on 2023-02-25 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportslifestyle', '0008_rename_create_at_order_date_ordered_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='variants',
        ),
    ]
