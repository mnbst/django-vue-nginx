# Generated by Django 2.2.8 on 2020-01-25 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_console', '0008_auto_20200125_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fetchsetting',
            old_name='user',
            new_name='authority',
        ),
    ]