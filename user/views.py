from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from user.forms import SignUpForm, LoginForm


def signup(request):
    if request.user:
        return redirect('/home/')
    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'user/sign_up.html', {'sign_up_form': form})
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    try:
        User.objects.get(email=email)
        return HttpResponse("User already with email, try login.")
    except User.DoesNotExist:
        user = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)
        )
        user.save()
        login(request, user)
        return redirect("/home/")


@login_required(login_url="/login/")
def home(request):
    return render(request, 'user/home.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def login_view(request):
    login_form = LoginForm()
    if request.method == "GET":

        return render(
            request, 'user/login.html', {'login': login_form}
        )
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(username=email, password=password)
    if user:
        login(request, user)
        return redirect("/home/")
    return render(
        request, "user/login.html",
        {
            "error_message": "Email or password is wrong",
            'login': login_form
        })
