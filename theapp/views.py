from django.shortcuts import render , redirect
from django.http import HttpResponse ,HttpResponseRedirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import requests
from bs4 import BeautifulSoup
from .gemini_helper import generate_response
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='imoo/login/')
def home(request):
    users = User.objects.all()
    return render(request, 'imoo/homepage.html', {'users': users})

def login_view(request):
    print("LOGIN VIEW:", request.method)
    print("POST DATA:", request.POST)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("USERNAME =", username, "PASSWORD =", password)

        user = authenticate(request, username=username, password=password)
        print("AUTH USER =", user)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            return render(request, 'imoo/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'imoo/login.html')

# @login_required(login_url='imoo/login/')
# def private_chat(request, username):
#     other_user = get_object_or_404(User, username=username)
#     return render(request, 'imoo/private_chat.html', {
#         'other_user': other_user,
#     })

def blank_page(request):
    return HttpResponseRedirect("about:blank")

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # user create with hashed password
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        # optional: auto login ya direct login page
        return redirect('login')

    return render(request, 'imoo/signup.html')

@login_required
def get_room_name(user1, user2):
    users = sorted([user1.username, user2.username])
    return f"{users[0]}__{users[1]}"

@login_required
def global_chat(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "imoo/global_room.html", {"users": users})

@login_required
def private_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    room_name = get_room_name(request.user, other_user)
    ctx = {
        "other_user": other_user,
        "room_name": room_name,
        "user": request.user,
    }
    return render(request, "imoo/private_room.html", ctx)

@login_required
@require_http_methods(["GET", "POST"])
def ai_doubt_solver(request):
    if request.method == "POST":
        doubt = request.POST.get("doubt", "").strip()
        if not doubt:
            return JsonResponse({"ai_answer": "Koi doubt nahi mila."}, status=400)

        ai_answer = generate_response(doubt)
        return JsonResponse({"ai_answer": ai_answer}, status=200)

    return render(request, "imoo/ai_doubt.html")