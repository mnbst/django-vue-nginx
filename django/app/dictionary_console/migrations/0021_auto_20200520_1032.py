# Generated by Django 3.0.6 on 2020-05-20 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary_console", "0020_auto_20200512_0330"),
    ]

    operations = [
        migrations.RenameField(
            model_name="video",
            old_name="excepted",
            new_name="has_caption",
        ),
    ]
