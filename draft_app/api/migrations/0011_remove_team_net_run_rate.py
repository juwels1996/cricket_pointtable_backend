# Generated by Django 5.1.6 on 2025-04-07 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_pdf_upload_date_pdf_date_pdf_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='net_run_rate',
        ),
    ]
