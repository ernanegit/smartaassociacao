# Generated by Django 5.2 on 2025-04-28 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atas', '0002_ata_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ata',
            name='slug',
        ),
    ]
