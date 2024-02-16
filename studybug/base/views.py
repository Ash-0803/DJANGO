from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm, UserForm, MyUserCreationForm
from .models import Message, Room, Topic, User

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try: 
            user = User.objects.get(email=email)
        except:
            messages.error(request,"User not found")
            
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Email OR password does not exist")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred while registering")
            
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"rooms": rooms, "topics": topics, "count":rooms_count, "room_messages": room_messages}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    
    # Message class is a child of class Room in models, so we can access all the messages, directly by this :
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') # it takes the value of "name =body" of the element in the form.
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)  # the page can still reload if we don't use this line, but since we used POST method, to make sure, nothing breaks up, we need to refresh the page.
    
    
    context = {"room": room, 'room_messages': room_messages, "participants": participants}
    return render(request, "base/room.html", context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()[0:5]

    context = { 'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics }
    return render(request,"base/profile.html",context)


@login_required(login_url="/login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    
    if request.method == "POST":
        # form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)    #if entered topic exists, it retruns that object, if not, it creates a new object
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        # this method can be used when using built-in forms to save. But since we manually created the form, we have to use the method shown above. 
        # if form.is_valid():
        #     room = form.save(commit=False) #used to give form "instance" without saving it.
        #     room.host = request.user
        #     room.save()

        return redirect("home")

    context = {"form": form, "topics": topics }
    return render(request, "base/room_form.html", context)

@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect("home")

    context = {"form": form,"topics":topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You can't delete anyone else's page. Do mind your own please")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj": room})

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete anyone else's message")

    if request.method == "POST":
        message.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj": message})

@login_required(login_url="login")
def updateUser(request):
    form = UserForm(instance = request.user)
    
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user-profile",pk=request.user.id)
    
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html',{'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})