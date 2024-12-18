# Generated by Django 5.1.3 on 2024-11-19 05:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0007_alter_log_session_alter_log_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="session",
            unique_together={("lecture", "user", "session_start", "session_end")},
        ),
    ]
