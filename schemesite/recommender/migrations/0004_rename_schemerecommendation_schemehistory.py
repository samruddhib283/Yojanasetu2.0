# Generated by Django 5.1.5 on 2025-04-12 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_schemerecommendation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SchemeRecommendation',
            new_name='SchemeHistory',
        ),
    ]
