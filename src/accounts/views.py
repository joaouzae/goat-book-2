from django.shortcuts import render, redirect
from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from accounts.forms import ListUserCreationForm


def login(request):
    if request.method == "POST":
        form = forms.AuthenticationForm(request)
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        print(type(user))
        print("email: ", email)
        if user is not None:
            auth_login(request, user)
            print("fez login")
        else:
            return redirect("login")
        return redirect("/")
    form = forms.AuthenticationForm(request)
    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        form = ListUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Optionally log in the user
            auth_login(request, user)
        else:
            print("erro de validação")
            print("form.errors: ", form.errors)
        return redirect("home")
    else:
        form = ListUserCreationForm()

    return render(request, "signup.html", {"form": form})
