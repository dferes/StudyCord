# from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm


def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room.html', context)


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()    # if the number of fields and variable types match as expected
            return redirect('home') # access by name instead of endpoint
    context = { 'form': form}
    return render(request, 'base/room_form.html', context) 


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # This will pre-fill the form fields with the instance of room that matches id=pk
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid(): 
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        print(room)
        room.delete() # removes the instance from the db
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room}) # this would be for a get request
