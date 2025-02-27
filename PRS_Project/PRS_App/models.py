from django.db import models

# python manage.py check -- to check validity of model
# python manage.py makemigrations prs_app
# python manage.py migrate

class Module(models.Model):
    module_code = models.IntegerField()
    title = models.CharField(max_length=50, default="Module Title")
    description = models.CharField(max_length=50, default="Description")
    def __str__(self):
        return u'%i - %s' % (self.module_code, self.title.title())

    
class Professor(models.Model):
    professor_id = models.IntegerField()
    first_name = models.CharField(max_length=50, default="First Name")
    last_name = models.CharField(max_length=50, default="Last Name")
    modules = models.ManyToManyField(Module)    
    
    def __str__(self):
        return u'%s %s' % (self.first_name.title(), self.last_name.title())

class ModuleInstance(models.Model): # takes consts from module and adds variable fields for date and current professors
    instance_id = models.IntegerField()
    module_code = models.IntegerField()
    year = models.DateField()
    semester = models.IntegerField()
    professors = models.ManyToManyField(Professor)
    
    def __str__(self):
        prof_names = ', '.join(prof.name for prof in self.professors.all()) 
        return f'{self.module_code} ({self.year.year}, {self.semester}): {prof_names}'


class Student(models.Model):
    student_id = models.IntegerField()
    first_name = models.CharField(max_length=50, default="First Name")
    last_name = models.CharField(max_length=50, default="Last Name")
    modules = models.ManyToManyField(ModuleInstance)
    
    def __str__(self):
        return u'%s %s' % (self.first_name.title(), self.last_name.title())
    
class Rating(models.Model): # this is not a good model lol
    student_id = models.IntegerField()
    professor_id = models.IntegerField()
    instance_id = models.IntegerField() # module instance id
    rating = models.FloatField()
    def __str__(self):
        return u'%i: %i, %i - %f' % (self.student_id, self.module_code, self.professor_id, self.rating)


# for admin: python manage.py createsuperuser

    