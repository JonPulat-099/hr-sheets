# Generated by Django 5.1.5 on 2025-01-28 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0002_alter_organization_candidate_sheet_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='candidate_sheet_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='vacancy_sheet_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
