# Generated by Django 5.0.1 on 2024-01-21 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theblog", "0011_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post", name="title_tag", field=models.CharField(max_length=255),
        ),
    ]
