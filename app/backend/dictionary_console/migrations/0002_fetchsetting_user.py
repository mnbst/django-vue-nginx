# Generated by Django 2.2.8 on 2020-01-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_console', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fetchsetting',
            name='user',
            field=models.CharField(default='1', max_length=30),
        ),
    ]