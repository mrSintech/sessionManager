"""
    Handy Tools
"""
import json
import string
import random
import datetime
import jdatetime

# RestFramework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Auth
from rest_framework_simplejwt.tokens import RefreshToken

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

# Dependencies
from django.views.static import serve
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

# =-=-=-=-=-=-=-=-=- Classes -=-=-=-=-=-=-=-=-=-=-= #
class JwtTools(RefreshToken):
    token_class = RefreshToken
    token = None
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
    
    @classmethod   
    def generate_jwt(cls, user):
        data = {}
        token = cls.token_class.for_user(user)
        data["refresh"] = str(token)
        data["access"] = str(token.access_token)
        
        return data
    
# =-=-=-=-=-=-=-=-=- Functions -=-=-=-=-=-=-=-=-=-=-= #
@api_view(['GET'])
@permission_classes([AllowAny,])
def public_media_access(request, url, document_root=None, show_indexes=False):

    url = 'public/'+url
    return serve(
        request, 
        url, 
        document_root, 
        show_indexes
    )

def georgian_to_persian(date, kind='obj'):
    timestmp = datetime.datetime.timestamp(date)
    jalili_date  = jdatetime.datetime.fromtimestamp(timestmp)
    
    if kind == 'josn':
        jalili_date = json.dumps(jalili_date, indent=4, sort_keys=True, default=str)
        jalili_date = json.loads(jalili_date)
    
    return jalili_date

def tz_free_date(date):
    date = date.split('.')
    date = datetime.datetime.strptime(date[0], "%Y-%m-%dT%H:%M:%S")
    date = date.astimezone(tz=self.tz).replace(tzinfo=None)
    return date

def str2bool(word):
    return word.lower() in ("true", "yes", "1")

def response_prepare(msg_container, success, data):
    # Preparing messages for app response
    if msg_container == None:
        msg = None
    
    else:
        msg = ''
        for item in msg_container:
            msg = str(msg)+str(item)+'\n'
        
    res = {
        'success'  : success,
        'messages' : msg,
        'data'     : data
    }
    
    return res

def create_session_token(data):
    # Generate Token
    s = SessionStore()
    s['login_token'] = data
    s.create()
    session_key = s.session_key
    # s = SessionStore(session_key=s.session_key)

    return session_key

def random_code_generator(str_length=6):
    lettersAndDigits = string.digits
    return ''.join(random.sample(lettersAndDigits, str_length))
 
def is_empty(data):
    # check if variable is empty
    if data == '' \
    or data == 'null' \
    or data == 'undefined' \
    or data == None:
        return True
    else:
        return False

def validate_phonenumber(number):
    # Shaping and validating phone number
    phonenumber = str(number)
    for i in range(0,3):
        if phonenumber.startswith("0"):
            phonenumber = phonenumber[1:]

        if phonenumber.startswith("+"):
            phonenumber = phonenumber[1:]

        if phonenumber.startswith("98"):
            phonenumber = phonenumber[2:]

    if len(phonenumber) != 10:
        return ('err')

    if not phonenumber.isdigit():
        return ('err')
    
    return int(phonenumber)