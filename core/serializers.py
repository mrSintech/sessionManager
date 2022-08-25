import jdatetime
import datetime
import json
import pytz

# RestFramework
from rest_framework import serializers

# Models
from .models import *

# Tools
from core import tools
from django.utils import timezone

class RoomPicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RoomPic
        fields = [
            'id',
            'pic',
            'pic_thumbnail'
        ]
        
class SessionRoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RoomInfo
        fields = [
            'key',
            'value'
        ]
        
class SessionRoomDemoSerializer(serializers.ModelSerializer):
    pics = RoomPicSerializer(many=True)
    info = SessionRoomInfoSerializer(many=True)
    
    class Meta:
        model  = SessionRoom
        fields = [
            'id',
            'is_active',
            'title',
            'pics',
            'capacity',
            'info'
        ]
   
class SessionRoomReservesSerializer(serializers.ModelSerializer):
    tz    = pytz.timezone('Asia/Kolkata')
    title = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    end   = serializers.SerializerMethodField()
    
    def get_title(self, obj): 
        return obj.departman.title
    
    def get_start(self, obj):
        date = obj.execute_datetime
        date = date.replace(tzinfo=timezone.utc).astimezone(tz=self.tz)
        return date
    
    def get_end(self, obj):
        session_date = obj.execute_datetime
        duration = obj.duration
        end_date = session_date + datetime.timedelta(hours=duration)
        end_date = end_date.replace(tzinfo=timezone.utc).astimezone(tz=self.tz)
        return end_date
    
    class Meta:
        model  = Reserve
        fields = [
            'id',
            'is_done',
            'title', # Departman
            'start',
            'duration',
            'end'
        ]     
     
class SessionRoomDetailSerializer(serializers.ModelSerializer):
    pics     = RoomPicSerializer(many=True)
    reserves = SessionRoomReservesSerializer(many=True)
    
    class Meta:
        model  = SessionRoom
        fields = [
            'id',
            'title',
            'pics',
            'is_active',
            'capacity',
            'info',
            'reserves'
        ]

class ReserveSerializer(serializers.ModelSerializer):
    room             = SessionRoomDemoSerializer()
    execute_datetime = serializers.SerializerMethodField()
    
    def get_execute_datetime(self, obj):
        session_date = obj.execute_datetime
        jalili_date  = tools.georgian_to_persian(session_date, kind='josn')
        
        return jalili_date
        
    class Meta:
        model  = Reserve
        fields = [
            'id',
            'is_done',
            'duration',
            'execute_datetime',
            'room'
        ]
        