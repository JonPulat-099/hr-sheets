# Generated by Django 5.1.5 on 2025-01-29 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0003_alter_organization_candidate_sheet_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='gender',
            field=models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], default='male', max_length=10),
        ),
        migrations.AddField(
            model_name='candidate',
            name='state',
            field=models.CharField(choices=[('progress', 'В Процессе'), ('accept', 'Одобрено'), ('reject', 'Отказано')], default='active', max_length=10),
        ),
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='status',
            field=models.CharField(choices=[('active', 'Актив'), ('inactive', 'Блокирован')], default='active', max_length=10),
        ),
        migrations.AddField(
            model_name='organization',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]
