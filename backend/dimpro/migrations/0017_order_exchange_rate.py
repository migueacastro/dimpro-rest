# Generated by Django 5.1.5 on 2025-02-08 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0016_delete_pricetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='exchange_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dimpro.exchangerate'),
        ),
    ]
