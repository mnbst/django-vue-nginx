# Generated by Django 3.0.4 on 2020-03-14 14:22

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FetchSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authority', models.CharField(default='super', max_length=30, unique=True)),
                ('excepted_href', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, null=True, size=None)),
                ('page_to_crawl', models.PositiveIntegerField(default=5)),
                ('language_limit', models.PositiveIntegerField(default=1)),
                ('minimum_sentence', models.PositiveIntegerField(default=10)),
                ('video_per_page', models.PositiveIntegerField(default=10)),
                ('video_to_delete', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, null=True, size=None)),
                ('video_to_renewal', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, null=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_href', models.CharField(max_length=10, unique=True)),
                ('video_img', models.CharField(max_length=20)),
                ('video_time', models.CharField(max_length=10)),
                ('video_title', models.CharField(max_length=50)),
                ('video_genre', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('youtubeID', models.CharField(max_length=20)),
                ('video_upload_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_ini', models.CharField(max_length=1)),
                ('word', models.CharField(max_length=50, unique=True)),
                ('word_imi', models.CharField(default='', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='WordAppearance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appearance', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(default=0), size=None)),
                ('video_href', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary_console.Video', to_field='video_href')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary_console.Word', to_field='word')),
            ],
        ),
        migrations.CreateModel(
            name='Caption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField(default=0)),
                ('start_time', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('end_time', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('text', models.CharField(max_length=100)),
                ('word', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('word_imi', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20, null=True), size=None)),
                ('video_href', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary_console.Video', to_field='video_href')),
            ],
        ),
    ]
