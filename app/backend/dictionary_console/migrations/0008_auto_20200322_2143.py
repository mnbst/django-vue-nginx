# Generated by Django 3.0.4 on 2020-03-22 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_console', '0007_auto_20200320_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word_ini',
            field=models.CharField(db_index=True, max_length=1),
        ),
    ]
