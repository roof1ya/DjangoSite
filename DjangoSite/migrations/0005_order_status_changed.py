# Generated by Django 5.1.5 on 2025-02-25 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoSite', '0004_order_change_status_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status_changed',
            field=models.BooleanField(default=False),
        ),
    ]
