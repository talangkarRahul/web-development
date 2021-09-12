from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from user.forms import SignUpForm, LoginForm, UserForm
from user.helper import user_handle


def home(request):
    return render(request, 'user/home.html', {'user': request.user})


def signup(request):

    if request.user.is_authenticated:
        return redirect("/user/profile/")

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


@login_required()
def profile(request):
    if request.method == "GET":
        user_form = UserForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })
        return render(request, 'user/profile.html', {'form': user_form})
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = request.user
            user.first_name = user_form.data['first_name']
            user.last_name = user_form.data['last_name']
            user.save()
            user_form = UserForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
            return render(request, 'user/profile.html', {
                'form': user_form,
                'message': "Profile updated successfully"
            })
        else:
            print(user_form.errors)
            return render(request, 'user/profile.html', {
                'form': user_form,
                'error': user_form.errors
            })


def logout_view(request):
    logout(request)
    return redirect('/login/')


def login_view(request):
    login_form = LoginForm()
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/user/profile")
        return render(
            request, 'user/login.html', {'login': login_form}
        )
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(username=email, password=password)
    if user:
        login(request, user)
        return redirect("/user/profile")
        # return user_handle(request)
    return render(
        request, "user/login.html",
        {
            "error_message": "Email or password is wrong",
            'login': login_form
        })
