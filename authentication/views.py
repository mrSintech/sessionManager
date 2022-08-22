# Rest Framework
from rest_framework.response import Response
from rest_framework import viewsets, status

# Models
from .models import *

# Serializers
from .serializers import *

class Test(viewsets.ViewSet):
    def list(self, request):
        user = User.objects.all()
        serializer = TestSerializer(user, many=True)
        
        return Response(serializer.data)
