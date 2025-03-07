# Generated by Django 5.1.6 on 2025-02-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("prs_app", "0002_remove_student_name_module_title_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rating",
            old_name="module_code",
            new_name="instance_id",
        ),
        migrations.AddField(
            model_name="module",
            name="description",
            field=models.CharField(default="Description", max_length=50),
        ),
        migrations.CreateModel(
            name="ModuleInstance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("instance_id", models.IntegerField()),
                ("module_code", models.IntegerField()),
                ("year", models.DateField()),
                ("semester", models.IntegerField()),
                ("professors", models.ManyToManyField(to="prs_app.professor")),
            ],
        ),
        migrations.AlterField(
            model_name="student",
            name="modules",
            field=models.ManyToManyField(to="prs_app.moduleinstance"),
        ),
    ]
