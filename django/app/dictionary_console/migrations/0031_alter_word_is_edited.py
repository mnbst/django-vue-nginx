# Generated by Django 3.2 on 2021-05-09 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary_console", "0030_word_is_edited"),
    ]

    operations = [
        migrations.AlterField(
            model_name="word",
            name="is_edited",
            field=models.BooleanField(default=True),
        ),
    ]
