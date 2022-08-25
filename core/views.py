import json

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
        # messages.append(str(request.POST))
        try:
            sessions = request.POST['session']
            messages.append(sessions)
            sessions = json.loads(sessions)
            # messages.append(sessions[0])
        except MultiValueDictKeyError:
            pass
        
        # for session in sessions:
        #     messages.append(session.title)
        
        res = tools.response_prepare(messages, True, None)
        return Response(res)
        
            