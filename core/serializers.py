import jdatetime
import datetime
import json

# RestFramework
from rest_framework import serializers

# Models
from .models import *

# Tools
from core import tools

class RoomPicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RoomPic
        fields = [
            'id',
            'pic',
            'pic_thumbnail'
        ]
        
class SessionRoomDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SessionRoom
        fields = [
            'id',
            'is_active',
            'title',
            'capacity'
        ]
        
class RoomDetailSerializer(serializers.ModelSerializer):
    pics = RoomPicSerializer(many=True)
    
    class Meta:
        model  = SessionRoom
        fields = [
            'id',
            'title',
            'pics',
            'is_active',
            'capacity',
            'has_heater',
            'has_cooler',
            'has_projector'
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
        