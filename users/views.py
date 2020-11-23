from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Create your views here.


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


def register(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = CustomUserCreationForm()
        context['form'] = form

    return render(request, 'users/register.html', context)
