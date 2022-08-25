import json
import pytz

# Rest Framework
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated, 
    IsAdminUser
)

# Models
from .models import *

# Serializers
from .serializers import *

# Tools
from django.utils import timezone
from core import tools

# Exceptions
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

class UserRoomReserveViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    
    def list(self, request):
        # Gathering data
        user     = request.user
        reserves = user.reserves.order_by('-execute_datetime')
        
        serializer = ReserveSerializer(reserves, many=True)
        
        return Response(serializer.data)
    
class RoomViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    
    def list(self, request):
        # Gathering data
        rooms = SessionRoom.actives.all()
        serializer = SessionRoomDemoSerializer(rooms, many=True)
        
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        room = SessionRoom.actives.get(id=pk)
        serializer = SessionRoomDetailSerializer(room)
        return Response(serializer.data)
   
    def create(self, request):
        is_valid = True
        messages = []
        
        try:
            sessions = request.POST['session']
            
        except MultiValueDictKeyError:
            pass
        
        sessions = json.loads(sessions)
        for session in sessions:
            try:
                session['id']
            
            except KeyError:
                title = session['title']
                start = session['start']
                end   = session['end']
           
        tz = timezone('Asia/Tehran')  
        start = start.split('.')
        start = datetime.datetime.strptime(start[0], "%Y-%m-%dT%H:%M:%S")
        start = start.astimezone(tz=tz)
        
        end = end.split('.')
        end = datetime.datetime.strptime(end[0], "%Y-%m-%dT%H:%M:%S")
        end = end.astimezone(tz=tz)
        
        res = tools.response_prepare(messages, True, None)
        return Response(res)
        
            