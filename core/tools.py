"""
    Handy Tools
"""
import string
import random

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

# Auth
from rest_framework_simplejwt.tokens import RefreshToken

# Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


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