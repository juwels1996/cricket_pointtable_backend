# Generated by Django 5.1.6 on 2025-03-21 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_youtubevideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='category',
            field=models.CharField(choices=[('Local', 'Local'), ('Semi-Local', 'Semi-Local'), ('Overseas', 'Overseas')], default='Local', max_length=20),
        ),
    ]
