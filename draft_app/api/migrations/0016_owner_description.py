# Generated by Django 5.1.6 on 2025-07-15 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_matchphotogallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
