# Generated by Django 5.1.5 on 2025-02-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoSite', '0002_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_surname',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]
