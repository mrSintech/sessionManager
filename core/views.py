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
   
    def _conflict_validator(self, start, end, room):
        is_valid = True
        reserve_conflicts = Reserve.objects.filter(
            (
                Q(room=room) &
                Q(execute_datetime__date=start.date())
            ) &
            (
                (
                    Q(execute_datetime__lt=end) &
                    Q(end_datetime__gt=end)
                ) |
                (
                    Q(execute_datetime__lt=start) &
                    Q(end_datetime__gt=start)
                ) |
                (
                    Q(execute_datetime__lt=start)&
                    Q(end_datetime__gt=end)
                ) |
                (
                    Q(execute_datetime__gt=start)&
                    Q(end_datetime__lt=end)
                ) |
                (
                    Q(execute_datetime=start)&
                    Q(end_datetime=end)
                )
            )
        )
        if len(reserve_conflicts) != 0:
            is_valid = False
        
        return is_valid
        
    def _reserve_validations(self, user, start, end, room):
        is_valid = True
        
        current_time = datetime.datetime.now() 
        # check reserve conflicts
        if not self._conflict_validator(start, end, room):
            is_valid = False
            self.messages.append(validation_msg.ReserveConflict)
        
        # check reserve in past
        time_dif = (start - current_time).total_seconds()
        if time_dif < 0:
            is_valid = False
            self.messages.append(validation_msg.ReserveInPastNotAllowed)
            
        # check end be grater than start
        if start > end:
            is_valid = False
            self.messages.append(validation_msg.ReserveTimeInvalid)
            
        # check day of reserve be close
        max_date = current_time + datetime.timedelta(days=settings.MAX_DAY_RANGE_TO_RESERVE)
        if end.date() > max_date.date():
            is_valid = False
            self.messages.append(validation_msg.ReserveDayRangeLimit)
            
        # reserve duration 
        self.duration = (end - start).total_seconds() / 3600
        
        if self.duration > settings.MAX_SESSION_TIME:
            is_valid = False
            self.messages.append(validation_msg.ReserveTimeLimited)
            
        # check user's other sessions in the same day
        reserves = user.reserves.filter(
            execute_datetime__date = start.date()
        )
        if len(reserves) >= settings.USER_MAX_SESSION_PER_DAY:
            is_valid = False
            self.messages.append(validation_msg.ReserveCountPerDayLimit)
            
        # check round time
        if start.minute != 0 \
            or start.second != 0 \
            or end.minute != 0 \
            or end.second != 0:
                is_valid = False
                self.messages.append(validation_msg.ReserveMinSecInvalid)
        
        return is_valid
    
    def tz_free_date(self, date):
        tz = pytz.timezone('Asia/Tehran')  
        date = date.split('.')
        date = datetime.datetime.strptime(date[0], "%Y-%m-%dT%H:%M:%S")
        date = date.astimezone(tz=tz).replace(tzinfo=None)
        return date
            
    def create(self, request):
        is_valid = True
        self.messages = []
        
        # messages.append(request.POST)
        # Gather data
        try:
            # load reserve json
            reserves = request.POST['session']
            reserves = json.loads(reserves)
            
            room = request.POST['room']
            room = SessionRoom.actives.get(id=room)
               
        except MultiValueDictKeyError:
            return Response(
                {'message':'required parameters missed!'},
                status=status.HTTP_400_BAD_REQUEST
            )
 
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
            start = self.tz_free_date(start)
            end   = self.tz_free_date(end)
            user  = request.user
            
            # validate reserve
            is_valid = self._reserve_validations(user, start, end, room)

            if is_valid:
                reserve = Reserve(
                    title=title,
                    reservatore=user,
                    room=room,
                    execute_datetime=start,
                    end_datetime=end,
                    duration=self.duration
                )
                reserve.save()
                            
                res = tools.response_prepare(self.messages, True, None)
                return Response(res)
        
        else: # no reserve date selected
            self.messages.append(validation_msg.ReserveNoDateSelected) 
        
        # FAIL
        res = tools.response_prepare(self.messages, False, None)
        return Response(res)
    