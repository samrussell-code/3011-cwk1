from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from prs_app.models import *
import traceback

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

def List(request):
    module_instances = ModuleInstance.objects.all()

    result = []
    for instance in module_instances:

        module_data = {
            "module_code": instance.module.module_code, 
            "module_name": instance.module.title, 
            "year": instance.year,  
            "semester": instance.get_semester_display(),  
            "professors": [
                {
                    "id": prof.id,  
                    "name": f"Professor {prof.first_name[0]}. {prof.last_name.title()}" 
                }
                for prof in instance.professors.all()  
            ]
        }
        result.append(module_data)
    return JsonResponse(result, safe=False)


def View(request):
    all_professors = Professor.objects.all()
    prof_map = {prof.id: f"{prof.first_name.title()} {prof.last_name.title()}" for prof in all_professors}
    ratings = Rating.objects.select_related("professor").values("professor_id", "rating")
    rating_map = {r["professor_id"]: r["rating"] for r in ratings}
    res = [
        {
            "professor": prof_map[prof.id],
            "id": prof.id,
            "rating": "*" * round(rating_map.get(prof.id, 0)),  # format rating as stars
            "avg_rating": round(rating_map.get(prof.id, 0), 2)  # show average rating rounded to 2 decimals
        }
        for prof in all_professors
    ]

    return JsonResponse(res, safe=False)



def Average(request):
    try:
        # expected format -> 'professor_id' and 'module_code' as GET parameters
        prof_id = request.GET.get('professor_id')  # get professor_id from query params
        mod_code = request.GET.get('module_code')  # get module_code from query params
        
        if not prof_id or not mod_code:
            return JsonResponse({"error": "Missing professor_id or module_code"}, status=400)

        # fetch professor name
        professor = Professor.objects.filter(id=prof_id).first()
        if not professor:
            return JsonResponse({"error": "Professor not found"}, status=404)

        professor_name = f"{professor.first_name.title()} {professor.last_name.title()}"
        
        # fetch the module instance
        module_instance = ModuleInstance.objects.filter(module__module_code=mod_code).first()
        if not module_instance:
            return JsonResponse({"error": "Module instance not found"}, status=404)

        module_name = module_instance.module.title  # Assuming 'title' is a field in the Module model
        ratings = Rating.objects.filter(professor_id=prof_id, module_instance=module_instance) 
        if not ratings.exists():
            return JsonResponse({"error": "No ratings found for this professor and module"}, status=404)
        avg_rating = ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        
        if avg_rating is None:
            return JsonResponse({"error": "No ratings available for this professor/module combination"}, status=404)

        rounded_rating = round(avg_rating)
        rating_stars = '*' * rounded_rating 
        return JsonResponse({
            "professor": professor_name,
            "id": prof_id,
            "rating": rating_stars,  # asterisks
            "avg_rating": rounded_rating,
            "module_name": module_name, 
            "module_code": mod_code, 
        })
    
    except Exception as e:
        error_message = traceback.format_exc()
        print(f"Error: {error_message}")
        return JsonResponse({"error": "An internal error occurred. Please check logs for details."}, status=500)


@csrf_exempt # this goes on top of all post req funcs
def Rate(request):
    return HttpResponse("rate")

