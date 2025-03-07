# Generated by Django 5.1.6 on 2025-03-02 12:52

import django.db.models.deletion
import prs_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prs_app", "0011_remove_student_email_remove_student_password_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                default=prs_app.models.get_default_user,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
