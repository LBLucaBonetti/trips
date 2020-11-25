from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm

# Create your views here.


def user_register(request):
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


def user_login(request):
    pass
