from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import Q
import json


from prs_app.models import *
import traceback

def HandleRegisterRequest(request):
    return HttpResponse("not yet implemented")

@csrf_exempt # this goes on top of all post req funcs
def Home(request):
    return HttpResponse("home")

@csrf_exempt
def Register(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if not username or not email or not password:
                return JsonResponse({"error": "username, email, and password required"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "username already taken"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "email already registered"}, status=400)

            hashed_password = make_password(password)

            # django user
            user = User.objects.create(username=username, email=email, password=hashed_password)

            # linked student (for storing models, is an extension of django user)
            student = Student.objects.create(user=user)

            return JsonResponse({"message": "registration successful", "student_id": student.id}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "must be POST"}, status=405)


@csrf_exempt # this goes on top of all post req funcs
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    else:
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

@csrf_exempt # this goes on top of all post req funcs
def Logout(request):
    if request.method == 'POST':  
        auth_logout(request)  # built-in logout 
        return HttpResponse("Logout successful", status=200)
    else:
        return HttpResponse("Invalid request method", status=405) # non-post
    
def List(request):
    module_instances = ModuleInstance.objects.all()

    result = []
    for instance in module_instances:
        module_data = {
            "module_code": instance.module.module_code,
            "module_name": instance.module.title,
            "year": instance.start_date.year,  # Get the year from start_date
            "semester": instance.get_semester_display(),
            "professors": [
                {
                    "id": prof.professor_id,  # Make sure you're returning professor_id
                    "name": f"Professor {prof.first_name[0]}. {prof.last_name.title()}"
                }
                for prof in instance.professors.all()
            ]
        }
        result.append(module_data)

    return JsonResponse(result, safe=False)

def View(request):
    all_professors = Professor.objects.all()
    prof_map = {prof.professor_id: f"{prof.first_name.title()} {prof.last_name.title()}" for prof in all_professors}
    
    res = []
    for prof in all_professors:
        ratings = Rating.objects.filter(professor=prof)
        
        if not ratings.exists():
            avg_rating = 0
        else:
            avg_rating = ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0
        
        rounded_rating = round(avg_rating)
        rating_stars = '*' * rounded_rating
        
        res.append({
            "professor": prof_map[prof.professor_id],  
            "id": prof.professor_id,  
            "rating": rating_stars,  
            "avg_rating": rounded_rating  
        })
    
    return JsonResponse(res, safe=False)





def Average(request):

    try:
        prof_id = request.GET.get('professor_id')
        mod_code = request.GET.get('module_code')

        if not prof_id or not mod_code:
            return JsonResponse({"error": "Missing professor_id or module_code"}, status=400)

        professor = Professor.objects.filter(professor_id=prof_id).first()
        if not professor:
            return JsonResponse({"error": "Professor not found"}, status=404)

        module_instance = ModuleInstance.objects.filter(module__module_code=mod_code).first()
        if not module_instance:
            return JsonResponse({"error": "Module instance not found"}, status=404)

        ratings = Rating.objects.filter(professor=professor, module_instance=module_instance)

        if not ratings.exists():
            avg_rating = 0  # set avg to 0 if no ratings
        else:
            avg_rating = ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0  # ensure avg is 0 if None

        rounded_rating = round(avg_rating)
        rating_stars = '*' * rounded_rating 
 
        return JsonResponse({
            "professor": f"{professor.first_name.title()} {professor.last_name.title()}",
            "id": prof_id,
            "rating": rating_stars,
            "avg_rating": rounded_rating,
            "module_name": module_instance.module.title,
            "module_code": mod_code,
        })

    except Exception as e:
        error_message = traceback.format_exc()
        print(f"ERROR: {error_message}")  
        return JsonResponse({"error": "An internal error occurred. Please check logs for details."}, status=500)



@login_required
@csrf_exempt
def Rate(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User must be logged in"}, status=401)

        data = json.loads(request.body)

        prof_id = data.get("professor_id")
        mod_code = data.get("module_code")
        year = data.get("year")  # year is string
        semester = data.get("semester")
        rating_value = data.get("rating")

        if not all([prof_id, mod_code, year, semester, rating_value]):
            return JsonResponse({"error": "Missing required parameters"}, status=400)

        try:
            year_date = f"{year}-01-01"  # need to do to store in model
            year = datetime.strptime(year_date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Year must be a valid date"}, status=400)

        try:
            rating_value = float(rating_value)
        except ValueError:
            return JsonResponse({"error": "Rating must be a valid number"}, status=400)

        if not (0 <= rating_value <= 5):
            return JsonResponse({"error": "Rating must be between 0 and 5"}, status=400)

        student = Student.objects.filter(user=request.user).first()
        if not student:
            return JsonResponse({"error": "Student profile not found"}, status=404)

        professor = Professor.objects.filter(professor_id=prof_id).first() 
        if not professor:
            return JsonResponse({"error": "Professor not found"}, status=404)


        module_instance = ModuleInstance.objects.filter(
            module__module_code=mod_code, semester=semester, start_date__year=year.year 
        ).first()

        if not module_instance:
            return JsonResponse({"error": "Module instance not found"}, status=404)

        existing_rating = Rating.objects.filter(
            student=student, professor=professor, module_instance=module_instance
        ).exists()

        if existing_rating:
            return JsonResponse({"error": "You have already rated this professor for this module instance"}, status=400)

        Rating.objects.create(
            student=student, professor=professor, module_instance=module_instance, rating=rating_value
        )

        return JsonResponse({
            "professor_id": prof_id,
            "module_code": mod_code,
            "year": str(year),  
            "semester": semester,
            "rating": rating_value
        }, status=201)

    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid input format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
