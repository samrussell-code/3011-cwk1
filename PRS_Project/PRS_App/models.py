from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import re

# python manage.py check -- to check validity of model
# python manage.py makemigrations prs_app
# python manage.py migrate

class Module(models.Model):
    module_code = models.CharField(max_length=3, unique=True, validators=[RegexValidator(r'^[a-zA-Z0-9]{3}$')])  # alphanumeric and 3 chars
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="Description")

    def __str__(self):
        return f"{self.module_code.upper()} - {self.title.title()}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['module_code'], name='unique_module_code')
        ]
    
    def save(self, *args, **kwargs): #module code not case sensitive
        self.module_code = self.module_code.upper()
        super(Module, self).save(*args, **kwargs)



class Professor(models.Model):
    professor_id = models.CharField(
        max_length=3, 
        unique=True, 
        validators=[RegexValidator(r'^[a-zA-Z0-9]{3}$')],
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['professor_id'], name='unique_professor_id')
        ]
        ordering = ['last_name']
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="instances", null=True, blank=True)
    start_date = models.DateField(
        validators=[
            MinValueValidator(datetime(1900, 1, 1).date()),  # minmax years for moduleinstances
            MaxValueValidator(datetime.now().date())  
        ], null=True,blank=True
    )
    semester = models.IntegerField(choices=[(1, "First"), (2, "Second")])
    professors = models.ManyToManyField(Professor, related_name="module_instances")

    def __str__(self):
        prof_names = ', '.join(p.first_name for p in self.professors.all())
        return f"{self.module.module_code if self.module else 'Unknown'} ({self.start_date.year}, Sem {self.semester}): {prof_names}"


def get_default_user():
    return User.objects.first().id

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # link djangouser to student
    modules = models.ManyToManyField("ModuleInstance", related_name="students") # these have to be set manually by admin

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # rating limits between 0 and 5?

    def __str__(self):
        return f"{self.student} rated {self.professor} for {self.module_instance}: {self.rating}"
