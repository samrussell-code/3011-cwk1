# Generated by Django 5.1.6 on 2025-02-27 17:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("prs_app", "0003_rename_module_code_rating_instance_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="modules",
        ),
    ]
