# Rest Framework
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated, 
    IsAdminUser
)

# Dependencies
from rest_framework_simplejwt.views import TokenObtainPairView

# Models
from .models import *

# Serializers
from .serializers import *

# Exceptions
from django.utils.datastructures import MultiValueDictKeyError

# Tools
from core import validation_msg
from core.tools import (
    is_empty,
    validate_phonenumber,
    JwtTools,
)

# Dev tools
from django.http import HttpResponse

class Test(viewsets.ViewSet):
    def list(self, request):
        user = User.objects.all()
        serializer = TestSerializer(user, many=True)
        
        return Response(serializer.data)

class UserLogin(viewsets.ViewSet):
    """
        User login by phonenumber
    """
    permission_classes = [AllowAny,]
    
    def create(self, request):
        is_valid = True
        messages = []

        # Receive and validate number
        number = request.POST.get('number')
        if is_empty(number): # check if number is empty
            is_valid = False
            messages.append(validation_msg.LoginFieldEmpty)
        
        else:
            number = validate_phonenumber(number) # validate and format phonenumber
            if number == 'err':
                is_valid = False
                messages.append(validation_msg.WrongPhoneNumber)
        
        if is_valid:
            
            user = UserPhoneNumber.objects.get(number=number).user
            token = JwtTools.generate_jwt(user)
            print(token)
            
        return HttpResponse(number)
        
    