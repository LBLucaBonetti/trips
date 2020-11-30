from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomUserLoginForm


# Create your views here.


def user_register(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            context["form"] = form
    elif request.method == "GET":
        form = CustomUserCreationForm()
        context["form"] = form

    return render(request, "users/register.html", context)


def user_login(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                context["form"] = form
        else:
            context["form"] = form
    elif request.method == "GET":
        form = CustomUserLoginForm()
        context["form"] = form

    return render(request, "users/login.html", context)
