from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from imaplib import _Authenticator
from .models import *

from unicodedata import category
from operator import ilshift

from django.utils.dateformat import DateFormat
from django.shortcuts import render, redirect
from django.utils.formats import get_format
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.db.models import Q

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


from django.contrib.auth import logout, authenticate, login
from django.core.files.storage import FileSystemStorage
from account.models import Account

import simplejson as json
from .forms import *
import requests
import base64
import random
import email
import math
import os
import re

# start of API part
@api_view(['GET'])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = AccountSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_track_time(request, roomId):
    room = get_object_or_404(Room, id=roomId)
    return Response({"track_timer": room.track_timer})

@api_view(['GET'])
def get_room_users(request, roomId):
    room = get_object_or_404(Room, id=roomId)
    users = room.user_set.all()
    serializer = AccountSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def remove_user_from_room(request, roomId, userId):
    try:
        room = Room.objects.get(id=roomId)
        user = User.objects.get(id=userId)
        room.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Room.DoesNotExist or User.DoesNotExist:
        return Response({"error": "Room or User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_user_to_room(request, roomId, userId):
    try:
        room = Room.objects.get(id=roomId)
        user = User.objects.get(id=userId)
        room.user_set.add(user)
        return Response(status=status.HTTP_201_CREATED)
    except Room.DoesNotExist or User.DoesNotExist:
        return Response({"error": "Room or User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def select_track(request, roomId, trackId):
    try:

        room = Room.objects.get(id=roomId)
        track = Song.objects.get(id=trackId)
        room.song = track.name
        room.save()
        print(room)
        return Response(status=status.HTTP_201_CREATED)
    except Room.DoesNotExist or trackId.DoesNotExist:
        return Response({"error": "Room or Song does not exist"}, status=status.HTTP_404_NOT_FOUND)
# END OF API PART




def sized_render(request, file_name, content):
    content = {}
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return render(request, f'mobile/{file_name}', content)
    else:
        return render(request, file_name, content)

def index_page(request):
    content = {}
    
    response = requests.get(f'http://127.0.0.1:8000/api/get_user/{request.user.id}')
    
    return render(request, 'index.html', content)
        
# user sector
def personalAccount_page(request):
    content = {}
    return render(request, "personalAccount.html")

def personalAccountTemplates_page(request, name):
    content = {}
    path = f"personalAccountTemplates/template{name}.html"   
    return render(request, path) 

def edit_profile(request):
    content = {}
    try:
        email = request.user
        person = Account.objects.get(email=email)
        if request.method == "POST":
            if request.FILES:
                file = request.FILES['profile_photo']
                filename = f"profile_{str(person.email)}"
                logoImageData = upload_image(file, filename)
                person.userImage = logoImageData[0]
                # shop.prevLogoImage = logoImageData[-1]
            if request.POST.get('first_name', None):
                person.first_name = request.POST['first_name']
            if request.POST.get('last_name', None):
                person.last_name = request.POST['last_name']
            if request.POST.get('phone', None):
                person.phone = request.POST['phone']
            if request.POST.get('city', None):
                person.city = request.POST['city']
            person.save()
            return HttpResponseRedirect("/edit/")
        else:
            content['user'] = person
            return render(request, "editProfile.html", content)
    except Account.DoesNotExist as e:
        raise Http404 from e


# enterance sector
def logout_view(request):
    content = {}
    logout(request)
    return HttpResponseRedirect("/")

def login_page(request):
    content = {}
    form = SignUpForm(request.POST)
    content = {
        'form': form
    }
    # enterance request
    if request.method == 'POST' and 'btnform2' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        elif request.POST.get('password') != '':
            print('Try again! username or password is incorrect')
            content['errors'] = 'Try again! username or password is incorrect'
    # registration request
    elif request.method == 'POST' and 'btnform1' in request.POST:
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            username = email
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password, first_name=first_name)
            return redirect('/login/')
        else:
            print(form.errors)

    return sized_render(request, 'signin.html', content)



def forgot_password_page(request):
    content = {}
    return render(request, 'forgotPassword.html')



def service_page(request):

    content = {}

    user = Account.objects.get(id=request.user.id)

    if request.method == 'POST' and 'AddRoom' in request.POST:
        print(request.POST)

        room = Room(
        name = request.POST['name'],
        amount_of_users = int(request.POST['amount_of_users']),
        song = "Shape of my heart",
        timer = 128,
        )
        room.save()

        return redirect('/service/')


    if request.method == 'POST' and 'AddToRoom' in request.POST:

        print(request.POST)
        user.room = int(request.POST['AddToRoom'])
        user.save()

        return redirect('/service/')

    if request.method == 'POST' and 'LeaveToRoom' in request.POST:

        user.room = 0
        user.save()

        return redirect('/service/')


    return sized_render(request, 'service.html', content)


def serviceTemplate_page(request, name):
    content = {}
    try :
        content['rooms'] = Room.objects.all()
    except:
        pass
    
    path = f"serviceTemplates/template{name}.html"

    
    return render(request, path, content)

def roomTemplate_page(request, name):
    content={}
    
    room = Room.objects.get(id=name)
    songs = Song.objects.all()
    user = Account.objects.get(id=request.user.id)
    content['room'] = room
    content['songs'] = [song for song in songs]
    
    if request.method == 'POST' and 'AddToRoom' in request.POST:

        user.room = name
        user.save()
        return HttpResponseRedirect(f'/service/room/{name}/')


    if request.method == 'POST' and 'LeaveToRoom' in request.POST:

        user.room = 0
        user.save()

        return HttpResponseRedirect(f'/service/room/{name}/')






    return render(request, 'room.html', content)




def partners_page(request):
    content = {}


    return render(request, 'showPartner.html')





