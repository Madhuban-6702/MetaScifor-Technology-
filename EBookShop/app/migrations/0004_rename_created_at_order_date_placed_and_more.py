# Generated by Django 4.2.4 on 2025-03-05 11:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='date_placed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='order',
            name='date_of_delivery',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 12, 11, 42, 52, 884877, tzinfo=datetime.timezone.utc)),
        ),
    ]
