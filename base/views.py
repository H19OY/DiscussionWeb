from django.shortcuts import redirect, render
from django.http import HttpResponse 
from .forms import RoomForm
from .models import Room,Topic
from django.db.models import Q

# Create your views here.
rooms=[
    {'id':1,'name': 'Let\'s Learn Python'},
    {'id':2,'name': 'Let\'s Learn C#'},
    {'id':3,'name': 'Let\'s Learn Java'},
]

context={
    'rooms':rooms
}



def home(request):

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms= Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics}
    return render(request,'base/home.html',context)

def room(request,pk):

    n=int(pk)
    room=Room.objects.get(id=n)
    t={'room':room}
    
    
    return render(request,'base/room.html',t)


def createRoom(request):
    form=RoomForm()
    if request.method =='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context={'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    
    
    return render(request,'base/room_form.html',context)


def deleteRoom(request,pk):

    room=Room.objects.get(id=pk)
    context={'it':room}
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',context)