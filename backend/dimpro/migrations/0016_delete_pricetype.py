# Generated by Django 5.1.5 on 2025-02-05 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0015_exchangecurrency_exchangerate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PriceType',
        ),
    ]
