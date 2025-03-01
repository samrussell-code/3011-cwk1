from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# python manage.py check -- to check validity of model
# python manage.py makemigrations prs_app
# python manage.py migrate

class Module(models.Model):
    module_code = models.IntegerField(unique=True)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="Description")
    def __str__(self):
        return f"{self.module_code} - {self.title.title()}"

    
class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    modules = models.ManyToManyField(Module, related_name="professors")  # allows Module.objects.get().professors

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="instances", null=True, blank=True)  # temp fix
    year = models.IntegerField()
    semester = models.IntegerField(choices=[(1, "Spring"), (2, "Fall")])
    professors = models.ManyToManyField(Professor, related_name="module_instances")

    def __str__(self):
        prof_names = ', '.join(p.first_name for p in self.professors.all())
        return f"{self.module.module_code if self.module else 'Unknown'} ({self.year}, Sem {self.semester}): {prof_names}"


class Student(models.Model):
    username = models.CharField(max_length=50, unique=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)  # Make password nullable initially
    email = models.EmailField(unique=True)
    modules = models.ManyToManyField(ModuleInstance, related_name="students")

    def __str__(self):
        return f"{self.username} ({self.email})"


    

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # enforce rating limits

    def __str__(self):
        return f"{self.student} rated {self.professor} for {self.module_instance}: {self.rating}"




# for admin: python manage.py createsuperuser

    