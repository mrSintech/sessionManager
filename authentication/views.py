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

# Models
from .models import *

# Serializers
from .serializers import *

# Exceptions
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

# Tools
from core import validation_msg
from core.tools import (
    is_empty,
    validate_phonenumber,
    JwtTools,
    random_code_generator,
    create_session_token,
    response_prepare
)
from core.sms_handler import SendSms

# Dev tools
from django.http import HttpResponse

# Tasks
from .tasks import *

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
            # search user
            try:
                user = UserPhoneNumber.objects.get(number=number).user
            
            except ObjectDoesNotExist:
                is_valid = False
                messages.append(validation_msg.LoginPhoneNotExists)
                
            if is_valid:
                token = JwtTools.generate_jwt(user)
                code  = random_code_generator(4)
                token_data = {
                    'sms_code'     : code,
                    'login'        : token
                }
                
                # Create Session Token
                session_key = create_session_token(token_data)
                
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
                res = response_prepare(messages, True, json_data)
                return Response(res)
            
            
        # Fail
        res = response_prepare(messages, False, None)
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
        if is_empty(token) or is_empty(code):
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
                    res = response_prepare(messages, True, json_data)
                    return Response(res)
                
            
        # FAIL
        res = response_prepare(messages, False, None)
        return Response(res)