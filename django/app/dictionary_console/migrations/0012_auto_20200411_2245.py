# Generated by Django 3.0.5 on 2020-04-11 13:45

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary_console", "0011_auto_20200411_1940"),
    ]

    operations = [
        migrations.AddField(
            model_name="wordappearance",
            name="video_href",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="dictionary_console.Video",
                to_field="video_href",
            ),
        ),
        migrations.AlterField(
            model_name="wordappearance",
            name="appearance",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(default=0), size=None
            ),
        ),
        migrations.RemoveField(
            model_name="caption",
            name="unique_id",
        ),
    ]
