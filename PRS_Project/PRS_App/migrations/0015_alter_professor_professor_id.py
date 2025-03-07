# Generated by Django 5.1.6 on 2025-03-02 14:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prs_app", "0014_alter_professor_options_professor_professor_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="professor",
            name="professor_id",
            field=models.CharField(
                max_length=3,
                unique=True,
                validators=[django.core.validators.RegexValidator("^[a-zA-Z0-9]{3}$")],
            ),
        ),
    ]
