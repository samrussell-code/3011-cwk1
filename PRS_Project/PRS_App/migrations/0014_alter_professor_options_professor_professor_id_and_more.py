# Generated by Django 5.1.6 on 2025-03-02 14:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prs_app", "0013_alter_student_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="professor",
            options={
                "ordering": ["last_name"],
                "verbose_name": "Professor",
                "verbose_name_plural": "Professors",
            },
        ),
        migrations.AddField(
            model_name="professor",
            name="professor_id",
            field=models.CharField(
                max_length=3,
                null=True,
                unique=True,
                validators=[django.core.validators.RegexValidator("^[a-zA-Z0-9]{3}$")],
            ),
        ),
        migrations.AlterField(
            model_name="module",
            name="module_code",
            field=models.CharField(
                max_length=3,
                unique=True,
                validators=[django.core.validators.RegexValidator("^[a-zA-Z0-9]{3}$")],
            ),
        ),
        migrations.AddConstraint(
            model_name="module",
            constraint=models.UniqueConstraint(
                fields=("module_code",), name="unique_module_code"
            ),
        ),
        migrations.AddConstraint(
            model_name="professor",
            constraint=models.UniqueConstraint(
                fields=("professor_id",), name="unique_professor_id"
            ),
        ),
    ]
