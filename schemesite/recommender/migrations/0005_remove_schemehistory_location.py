# Generated by Django 5.1.5 on 2025-04-12 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0004_rename_schemerecommendation_schemehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schemehistory',
            name='location',
        ),
    ]
