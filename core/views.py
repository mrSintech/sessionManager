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
from django.db.models import Q


# Serializers
from .serializers import *

# Tools
from django.utils import timezone
from core import tools

# Dependencies
from core import validation_msg

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
        
        # Gather data
        try:
            reserves = request.POST['session']
            room     = request.POST['room']
            
        except MultiValueDictKeyError:
            return Response(
                {'message':'required parameters missed!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        room = SessionRoom.actives.get(id=room)
        
        # load json
        reserves = json.loads(reserves)
        
        # check for new session
        is_valid = False
        for reserve in reserves:
            try:
                reserve['id']
            
            except KeyError:
                title = reserve['title']
                start = reserve['start']
                end   = reserve['end']
                is_valid = True
        
        if is_valid:
            # timezone process
            tz = pytz.timezone('Asia/Tehran')  
            start = start.split('.')
            start = datetime.datetime.strptime(start[0], "%Y-%m-%dT%H:%M:%S")
            start = start.astimezone(tz=tz).replace(tzinfo=None)
            
            end = end.split('.')
            end = datetime.datetime.strptime(end[0], "%Y-%m-%dT%H:%M:%S")
            end = end.astimezone(tz=tz).replace(tzinfo=None)
            
            # check reserve time
            reserve_conflics = Reserve.objects.filter(
                execute_datetime__lt=start,
                end_datetime__gt=end
            )
            
            ser = ReserveSerializer(reserve_conflics, many=True)
            return Response(ser.data)
        
            # calculate duration
            duration = (end - start).total_seconds() / 3600
            
            user = request.user
            reserve = Reserve(
                title=title,
                reservatore=user,
                room=room,
                execute_datetime=start,
                end_datetime=end,
                duration=duration
            )
            reserve.save()
                        
            res = tools.response_prepare(messages, True, None)
            return Response(res)
        
        else: # no reserve date selected
            messages.append(validation_msg.ReserveNoDateSelected) 
        
        # FAIL
        res = tools.response_prepare(messages, False, None)
        return Response(res)