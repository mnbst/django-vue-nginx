# Generated by Django 2.2.10 on 2020-02-15 14:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_console', '0003_auto_20200215_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordappearance',
            name='appearance',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]