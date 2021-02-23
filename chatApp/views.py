from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .helpers import (is_authenticated, is_valid, is_user_of_content,
                      is_not_authenticated, is_created)
from .models import Message


@is_authenticated('app-chat')
def login(request):
    if request.method == 'GET':
        return render(request, 'chat/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        room_name = request.POST.get('room_name')
        request.session['room_name'] = room_name
        user = auth.authenticate(request,
                                 username=username,
                                 password=password)

        # Wrong password, or username does not exist
        if user is None:
            return redirect(reverse('login'))

        # Successful authentication, remember it
        auth.login(request, user)

        return redirect(reverse('app-chat'))


def logout(request):
    # In any case, attempt logout and
    # redirect to login page.
    auth.logout(request)
    return redirect(reverse('login'))


@is_authenticated('app-chat')
def create_user(request):
    if request.method == 'GET':
        return render(request, 'chat/create_user.html')

    if request.method == 'POST':
        # username is the only crucial parameter
        # for validation
        username = request.POST.get('username')
        if (not is_valid(username)) or is_created(username):
            return redirect(reverse('create-user'))

        # It is safe to create the user
        # Get post values and pass them to user
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            password=request.POST.get('password'),
        )
        user.save()
        auth.login(request, user)

        return redirect(reverse('logout'))


# Basic API actions

@is_not_authenticated('login')
def chat(request):
    if request.method == 'GET':
        # Pass the username to display it in the title
        # of the chat.
        room_name = request.session['room_name'].replace(" ", "").upper()
        context = {'username': request.user.username, 'room_name': room_name}
        return render(request, 'chat/room.html', context)





