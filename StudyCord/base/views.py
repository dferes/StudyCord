# from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # if user: adds the session inside the database and browser
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # do not commit to db yet; need to clean data
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration') # look for more specific error later
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name__icontains=q) # the i means case insensitive, contains means substring exists in the string
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) 

    topics = Topic.objects.all()
    room_count = rooms.count()  # apparently, getting the length of a query set is faster than python's len()
    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {
        'rooms': rooms, 
        'topics': topics, 
        'room_count': room_count,
        'room_messages': room_messages
    }
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # It is possible to query the child objects related to an instance of a parent model; in this case:
    # the parent model is Room (lowercase). We specify an instance of the parent model,
    # the 'room' variable above, and can then use the methods 'get', 'filter', 'exclude', etc.
    
    # room_messages = room.message_set.all().order_by('-created')
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room = room,
            body=request.POST.get('body')
        ) 
        room.participants.add(request.user)  # A little confused about how this line works, but it adds user info to the "Paricipants" tab in the room page
        return redirect('room', pk=room.id)

    context = {
        'room': room, 
        'room_messages': room_messages, 
        'participants': participants
    }
    return render(request, 'room.html', context)


@login_required(login_url='/login')  # If the session id is not in the browser then user will be redirected
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        print(f"topic: {topic} created: {created}")
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home') # access by name instead of endpoint
    context = { 'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context) 


@login_required(login_url='/login')  # If the session id is not in the browser then user 
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # This will pre-fill the form fields with the instance of room that matches id=pk
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')  # If the session id is not in the browser then user 
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete() # removes the instance from the db
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room}) # this would be for a get request
 

@login_required(login_url='/login')  # If the session id is not in the browser then user 
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete() # removes the instance from the db
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message}) # this would be for a get request


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  # all rooms that the user CREATED ??
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user, 
        'rooms': rooms, 
        'room_messages': room_messages,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)
 