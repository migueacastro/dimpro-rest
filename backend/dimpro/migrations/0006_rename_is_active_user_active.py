# Generated by Django 5.1.5 on 2025-01-16 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dimpro', '0005_alter_user_phonenumber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_active',
            new_name='active',
        ),
    ]
