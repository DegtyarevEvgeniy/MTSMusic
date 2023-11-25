from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import requests

# start of API part
@api_view(['GET']) # test api get time
def get_beta_server_time(request):
    try:
        beta_server = BetaServer.objects.first()  # Assuming you have only one BetaServer instance
        serializer = BetaServerSerializer(beta_server)
        return Response(serializer.data)
    except BetaServer.DoesNotExist:
        return Response({"error": "BetaServer does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)  # Assuming you have user authentication
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackTimeView(APIView):
    def get(self, request, roomId):
        room = Room.objects.get(pk=roomId)
        return Response({"track_timer": room.timer})

class RoomUsersView(APIView):
    def get(self, request, roomId):
        room = Room.objects.get(pk=roomId)
        users = room.user_set.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
def remove_user_from_room(request, roomId, userId):
    try:
        room = Room.objects.get(pk=roomId)
        user = User.objects.get(pk=userId)
        room.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Room.DoesNotExist or User.DoesNotExist:
        return Response({"error": "Room or User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_user_to_room(request, roomId, userId):
    try:
        room = Room.objects.get(pk=roomId)
        user = User.objects.get(pk=userId)
        room.user_set.add(user)
        return Response(status=status.HTTP_201_CREATED)
    except Room.DoesNotExist or User.DoesNotExist:
        return Response({"error": "Room or User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def select_track(request, roomId):
    try:
        room = Room.objects.get(pk=roomId)
        # Assuming you have a field named 'selected_track' in your Room model
        room.selected_track = request.data.get('selected_track', '')
        room.save()
        return Response(status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({"error": "Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
# END OF API PART


# START OF HTML CONTENT
def index_page(request):
    try:
        response = requests.get('http://127.0.0.1:8000/api/beta-server-time')  # Replace with your actual API URL
        response.raise_for_status()  # Check for any request errors

        beta_server_data = response.json()
        print(beta_server_data)
        return render(request, 'index.html', {'beta_server': beta_server_data})
    except requests.RequestException as e:
        return render(request, 'index.html', {'error': f'Error fetching data: {e}'})
    
def simple_func(request):
    print("\nThis is a simple function\n")
    return HttpResponse("""<html><script>alert('hello')</script></html>""")

