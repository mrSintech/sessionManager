import json

# Rest Framework
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated, 
    IsAdminUser
)

# Dependencies
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate

# Permissions
from core.permissions import IsStaff

# Models
from .models import *

# Serializers
from .serializers import *

# Exceptions
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

# Tools
from core import validation_msg
from core import tools
from core.sms_handler import SendSms

# Dev tools
from django.http import HttpResponse

# Tasks
from .tasks import *

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
        if tools.is_empty(number): # check if number is empty
            is_valid = False
            messages.append(validation_msg.LoginFieldEmpty)
        
        else:
            number = tools.validate_phonenumber(number) # validate and format phonenumber
            if number == 'err':
                is_valid = False
                messages.append(validation_msg.WrongPhoneNumber)
        
        if is_valid:
            # search user
            try:
                user = UserPhoneNumber.objects.get(number=number).user
            
            except ObjectDoesNotExist:
                is_valid = False
                messages.append(validation_msg.LoginPhoneNotExists)
                
            if is_valid:
                token = tools.JwtTools.generate_jwt(user)
                code  = tools.random_code_generator(4)
                token_data = {
                    'sms_code'     : code,
                    'login'        : token
                }
                
                # Create Session Token
                session_key = tools.create_session_token(token_data)
                
                # Send sms
                send_auth_sms.delay(number, code)
                
                # data serialize
                data = {
                    'username' : user.username,
                    'phonenumber' : number,
                    'token' : session_key
                }
                raw_data = json.dumps(data)
                json_data = json.loads(raw_data)
                     
                # SUCCESS
                messages.append(validation_msg.LoginSmsSent)
                res = tools.response_prepare(messages, True, json_data)
                return Response(res)
            
            
        # Fail
        res = tools.response_prepare(messages, False, None)
        return Response(res)
      
class LoginVerify(viewsets.ViewSet):
    permission_classes = [AllowAny,]
    
    def create(self, request):
        is_valid = True
        messages = []
        
        # Gathering data
        token = request.POST.get('token')
        code = request.POST.get('code')
        
        # Validating Data
        if tools.is_empty(token) or tools.is_empty(code):
            is_valid = False
            messages.append(validation_msg.SomethingWentWrong)
            
        if is_valid:
            # Unpack Session
            try:
                token_obj = Session.objects.get(pk=token)
                token_data = token_obj.get_decoded()

            except ObjectDoesNotExist:
                is_valid = False
                messages.append(validation_msg.LoginTokenExpired)
                
            if is_valid:
                if code != token_data['login_token']['sms_code']:
                    is_valid = False
                    messages.append(validation_msg.LoginIncorrectCode)
                    
                if is_valid:
                    # delete session obj after successful login
                    token_obj.delete()
                    
                    # declare tokens and serialize
                    jwt = token_data['login_token']['login']
                    raw_data = json.dumps(jwt)
                    json_data = json.loads(raw_data)
                    
                    # SUCCESS
                    messages.append(validation_msg.LoginSuccesful)
                    res = tools.response_prepare(messages, True, json_data)
                    return Response(res)
                
            
        # FAIL
        res = tools.response_prepare(messages, False, None)
        return Response(res)
    
class AdminLogin(viewsets.ViewSet):
    permission_classes = [AllowAny,]
    
    def create(self, request):
        is_valid = True
        messages = []
        
        # Gather data
        try:
            number   = request.POST['user']
            password = request.POST['pass']
            
        except MultiValueDictKeyError:
            return Response(
                {'message':'required parameters missed!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate number
        number = tools.validate_phonenumber(number)
        if number == 'err':
            is_valid = False
            messages.append(validation_msg.WrongPhoneNumber)
        
        if is_valid:  
            # Authenticate user  
            username = User.objects.get(phone_no__number=number).username
            user     = authenticate(username=username, password=password)
            
            if user:
                # Checking user admin
                try:
                    user.admin
                    
                except ObjectDoesNotExist:
                    is_valid = False
                
                if is_valid:
                    # admin authenticated, getting JWT
                    token = tools.JwtTools().generate_jwt(user)
                    res = tools.response_prepare(messages, True, token)
                    return Response(res)
            
            else:
                is_valid = False
                messages.append(validation_msg.LoginIncorrect)
        
        res = tools.response_prepare(messages, False, None)
        return Response(res)
    
class DepartmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    
    def list(self, request):
        departments = Departman.objects.all()
        serializer = DepartmentSeralizer(departments, many=True)
        return Response(serializer.data)
