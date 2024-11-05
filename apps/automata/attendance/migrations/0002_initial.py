# Generated by Django 5.1.2 on 2024-11-05 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("attendance", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="log",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="session",
            name="lecture",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="attendance.lecture"
            ),
        ),
        migrations.AddField(
            model_name="session",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="attendance.session"
            ),
        ),
        migrations.AddField(
            model_name="log",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="attendance.session"
            ),
        ),
        migrations.AddField(
            model_name="ble",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="attendance.session"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="session",
            unique_together={("lecture", "user")},
        ),
        migrations.AlterUniqueTogether(
            name="room",
            unique_together={("name", "building")},
        ),
        migrations.AlterUniqueTogether(
            name="ble",
            unique_together={("uuid", "major", "minor")},
        ),
    ]
