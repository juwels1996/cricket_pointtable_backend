# Generated by Django 5.1.6 on 2025-03-23 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_match_status_alter_match_team1_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='win_by_runs',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='win_by_wickets',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
