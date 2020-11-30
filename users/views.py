from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from trips.utils import user_is_authenticated
from users.forms import CustomUserCreationForm, CustomUserLoginForm


# Create your views here.


def user_register(request):
    context = {}

    if user_is_authenticated(request):
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

    if user_is_authenticated(request):
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


@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
