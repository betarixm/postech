# Generated by Django 5.1.3 on 2024-11-06 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0004_lecture_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="session",
            options={"ordering": ("-session_start",)},
        ),
    ]
