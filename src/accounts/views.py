from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from accounts.models import User


def login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if user := authenticate(request, email=email, password=password):
            auth_login(request, user)
        else:
            messages.error(request, "Invalid email or password")
        return redirect("/")
    return render(request, "login.html")


def logout(request: HttpRequest):
    auth_logout(request)
    return redirect("/")


def signup(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return redirect("/")
        # print("email: ", email)
        # print("password1: ", password1)
        user = authenticate(request, email=email, password=password1)
        # print("user: ", user)
        if user is None:
            user: User = User.objects.create_user(email)
            user.set_password(password1)
            user.save()
        auth_login(request, user)
        # print(type(user))
        # print("user.email: ", user.email)
        # print("user.is_authenticated: ", user.is_authenticated)
        return redirect("/")
    return render(request, "signup.html")
