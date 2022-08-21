from rest_framework import serializers

# Models
from .models import *

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[
            'id',
            'username',
            'email'
        ]