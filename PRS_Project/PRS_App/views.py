from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from prs_app.models import *

def HandleRegisterRequest(request):
    return HttpResponse("not yet implemented")

@csrf_exempt # this goes on top of all post req funcs
def Home(request):
    return HttpResponse("home")

@csrf_exempt # this goes on top of all post req funcs
def Register(request):
    return HttpResponse("register")

@csrf_exempt # this goes on top of all post req funcs
def Login(request):
    return HttpResponse("login")

@csrf_exempt # this goes on top of all post req funcs
def Logout(request):
    return HttpResponse("logout")


def List(request): # list all module instances, form: NAME, YEAR, SEMESTER, TEACHERS[]
    module_instances = ModuleInstance.objects.all().values("module_code", "year", "semester", "professors")
    return JsonResponse(list(module_instances), safe=False) #returns list instead of dict

@csrf_exempt # this goes on top of all post req funcs
def View(request):
    return HttpResponse("view")

@csrf_exempt # this goes on top of all post req funcs
def Average(request):
    return HttpResponse("average")

@csrf_exempt # this goes on top of all post req funcs
def Rate(request):
    return HttpResponse("rate")





