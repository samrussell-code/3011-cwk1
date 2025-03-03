# Generated by Django 5.1.6 on 2025-03-03 12:06

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "prs_app",
            "0017_remove_moduleinstance_year_moduleinstance_start_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="moduleinstance",
            name="start_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(datetime.date(1900, 1, 1)),
                    django.core.validators.MaxValueValidator(datetime.date(2025, 3, 3)),
                ],
            ),
        ),
    ]
