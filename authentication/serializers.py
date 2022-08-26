from rest_framework import serializers

# Models
from .models import *

class DepartmentSeralizer(serializers.ModelSerializer):
    class Meta:
        model  = Departman
        fields = [
            'id',
            'title',
        ]
        
