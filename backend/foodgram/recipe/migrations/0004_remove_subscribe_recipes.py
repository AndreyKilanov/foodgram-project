# Generated by Django 3.2 on 2023-04-06 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20230407_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribe',
            name='recipes',
        ),
    ]
