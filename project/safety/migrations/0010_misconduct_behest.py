# Generated by Django 5.2 on 2025-04-10 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safety', '0009_rename_protocol_path_misconduct_protocol'),
    ]

    operations = [
        migrations.AddField(
            model_name='misconduct',
            name='behest',
            field=models.FileField(blank=True, null=True, upload_to='generated/safety/'),
        ),
    ]
