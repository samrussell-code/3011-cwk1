from django.contrib import admin
from .models import *

# python manage.py runserver

admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Rating)