# Generated by Django 3.0.5 on 2020-05-02 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary_console", "0013_auto_20200421_1914"),
    ]

    operations = [
        migrations.CreateModel(
            name="CaptionWord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.IntegerField(default=0)),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.AlterModelOptions(
            name="caption",
            options={"ordering": ["index"]},
        ),
        migrations.AlterModelOptions(
            name="video",
            options={"ordering": ["video_upload_date"]},
        ),
        migrations.AlterModelOptions(
            name="word",
            options={"ordering": ["word"]},
        ),
        migrations.RemoveField(
            model_name="caption",
            name="meanings",
        ),
        migrations.RemoveField(
            model_name="caption",
            name="video_href",
        ),
        migrations.AddField(
            model_name="caption",
            name="video",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dictionary_console.Video",
            ),
        ),
        migrations.AddField(
            model_name="word",
            name="ng",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="caption",
            name="text",
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name="caption",
            name="words",
        ),
        migrations.DeleteModel(
            name="WordAppearance",
        ),
        migrations.AddField(
            model_name="captionword",
            name="caption",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="dictionary_console.Caption",
            ),
        ),
        migrations.AddField(
            model_name="captionword",
            name="word",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="dictionary_console.Word",
            ),
        ),
        migrations.AddField(
            model_name="caption",
            name="words",
            field=models.ManyToManyField(
                blank=True,
                through="dictionary_console.CaptionWord",
                to="dictionary_console.Word",
            ),
        ),
    ]
