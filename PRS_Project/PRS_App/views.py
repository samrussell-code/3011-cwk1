from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def HandleRegisterRequest(request):
    return HttpResponse("not yet implemented")

@csrf_exempt # this goes on top of all post req funcs
def Register(request):
    return HttpResponse("register")


