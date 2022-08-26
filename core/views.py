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
   
    def conflict_validator(self):
            reserve_conflicts = Reserve.objects.filter(
                (
                    Q(room=self.room) &
                    Q(execute_datetime__date=self.start.date())
                ) &
                (
                    (
                        Q(execute_datetime__lt=self.end) &
                        Q(end_datetime__gt=self.end)
                    ) |
                    (
                        Q(execute_datetime__lt=self.start) &
                        Q(end_datetime__gt=self.start)
                    ) |
                    (
                        Q(execute_datetime__lt=self.start)&
                        Q(end_datetime__gt=self.end)
                    ) |
                    (
                        Q(execute_datetime__gt=self.start)&
                        Q(end_datetime__lt=self.end)
                    ) |
                    (
                        Q(execute_datetime=self.start)&
                        Q(end_datetime=self.end)
                    )
                )
            )
            if len(reserve_conflicts) != 0:
                return False
            
            else:
                return True
   
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
        
        self.room = SessionRoom.actives.get(id=room)
        
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
            # timezone process # TODO: refactor
            tz = pytz.timezone('Asia/Tehran')  
            start = start.split('.')
            start = datetime.datetime.strptime(start[0], "%Y-%m-%dT%H:%M:%S")
            self.start = start.astimezone(tz=tz).replace(tzinfo=None)
            
            end = end.split('.')
            end = datetime.datetime.strptime(end[0], "%Y-%m-%dT%H:%M:%S")
            self.end = end.astimezone(tz=tz).replace(tzinfo=None)
            
            # check other reserve conflicts
            if not conflict_validator():
                is_valid = False
                messages.append(validation_msg.ReserveConflict)
               
            current_time = datetime.datetime.now() 
            # check reserve in past
            time_dif = (start - current_time).total_seconds()
            if time_dif < 0:
                is_valid = False
                messages.append(validation_msg.ReserveInPastNotAllowed)
                
            # check reserve duration limit
            duration = (end - start).total_seconds() / 3600
            
            if duration > settings.MAX_SESSION_TIME:
                is_valid = False
                messages.append(validation_msg.ReserveTimeLimited)
            
            # check day of reserve be close
            max_date = current_time + datetime.timedelta(days=settings.MAX_DAY_RANGE_TO_RESERVE)
            if end.date() > max_date.date():
                is_valid = False
                messages.append(validation_msg.ReserveDayRangeLimit)
            
            # check end be grater than start
            if start > end:
                is_valid = False
                messages.append(validation_msg.ReserveTimeInvalid)
            
            # check user's other sessions in the same day
            user     = request.user
            reserves = user.reserves.filter(
                execute_datetime__date = start.date()
            )
            if len(reserves) >= settings.USER_MAX_SESSION_PER_DAY:
                is_valid = False,
                messages.append(validation_msg.ReserveCountPerDayLimit)
        
            # check round time
            if start.minute != 0 \
                or start.second != 0 \
                or end.minute != 0 \
                or end.second != 0:
                    is_valid = False
                    messages.append(validation_msg.ReserveMinSecInvalid)
            
            if is_valid:
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
    