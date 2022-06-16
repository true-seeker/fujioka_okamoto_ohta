from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from voter.forms import LoginForm


def index(request):
    print(request.user)
    return HttpResponse(render(request, 'voter.html'))


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'voter.html')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    elif request.method == 'GET':
        return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        if len(User.objects.filter(username=request.POST['login'])) != 0:
            return render(request, 'signup.html', {'error': 'user already exists'})

        new_user = User.objects.create_user(username=request.POST['login'], password=request.POST['password'])
        new_user.save()
        login(request, new_user)
        return redirect('/voter')
        # return render(request, 'signup.html')
    elif request.method == 'GET':
        return render(request, 'signup.html')
