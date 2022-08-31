# Dependecies
from rest_framework.test import APITestCase
from django.contrib.sessions.models import Session

# Models
from authentication.models import *

# Tools
from core import tools

phonenumber = '9120000000'

class LoginTest(APITestCase):
    
    @staticmethod
    def get_token(user):
        auth = tools.JwtTools().generate_jwt(user)
        return auth['access']
    
    @staticmethod
    def create_temp_user():
        number = tools.random_code_generator(10).replace('0', '9', 1)
  
        # create phopnenumber
        num_model   = UserPhoneNumber(
            number=number,
        )
        num_model.save()
        
        # create departman
        dep = Departman(
            title='temp'
        )
        dep.save()
        
        # create user model
        user = User(
            phone_no=num_model,
            departman=dep
        )
        user.set_password('123456789')
        user.save()
        return user
    
    # @staticmethod
    def user_login(self):
        # create user
        user = self.create_temp_user()
        number = user.phone_no.number
        
        url = '/auth/login/'
        payload = {
            'number': number
        }
        
        # sending request
        req = self.client.post(url, payload).json()

        self.assertTrue(req['success'])
        # print(req)
        return req['data']['token']

    def test_login_verify(self):
        # gathering data
        token      = self.user_login()
        token_obj  = Session.objects.get(pk=token)
        token_data = token_obj.get_decoded()
        code       = token_data['login_token']['sms_code']
        
        # shaping request
        url     = '/auth/verify/'
        payload = {
            'token': token,
            'code' : code
        }
        
        req = self.client.post(url, payload).json()
        
        # testing
        self.assertEqual(req['success'], True)
        assert 'access' in req['data']
        
        return req['data']['access']
    
class AdminOperationsTest(APITestCase):
    @staticmethod
    def create_temp_user():
        number = tools.random_code_generator(10).replace('0', '9', 1)
        # create phopnenumber
        num_model = UserPhoneNumber(
            number=unmber,
        )
        num_model.save()
        
        # create departman
        dep = Departman(
            title='temp'
        )
        dep.save()
        
        # create user model
        user = User(
            phone_no=num_model,
            departman=dep
        )
        user.set_password('123456789')
        user.save()
        return user
    
    @staticmethod
    def create_admin_model():
        number = tools.random_code_generator(10).replace('0', '9', 1)
        # create phopnenumber
        num_model   = UserPhoneNumber(
            number=number,
        )
        num_model.save()
        
        # create departman
        dep = Departman(
            title='temp'
        )
        dep.save()
        
        # create user model
        user = User(
            phone_no=num_model,
            departman=dep
        )
        user.set_password('123456789')
        user.save()
        
        admin  = Admin(
            user=user
        ).save()
        
        return user

    def create_admin_user(self):
        user = self.create_admin_model()
        
        # get token
        url    = '/auth/a_login/'
        payload = {
            'user': user.username,
            'pass': '123456789'
        }
        
        req = self.client.post(url, payload).json()
  
        return req['data']['access']
     
    def test_admin_create_user(self):
        # run dependencies
        token = self.create_admin_user()
        
        dep = Departman.objects.last()
        # shaping request
        url     = '/auth/add_user/'
        payload = {
            'is_staff'  : False,
            'first_name': 'temp',
            'last_name' : 'temp',
            'number'    : '9121111111',
            'department': dep.id
        }
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.post(url, payload, **auth_headers).json()
        self.assertEqual(req['success'], True)
        
    def test_admin_create_staff_user(self):
        # run dependencies
        token = self.create_admin_user()
        
        dep = Departman.objects.last()
        # shaping request
        url     = '/auth/add_user/'
        payload = {
            'is_staff'  : True,
            'first_name': 'temp',
            'last_name' : 'temp',
            'number'    : '9121111112',
            'department': dep.id
        }
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.post(url, payload, **auth_headers).json()
        self.assertEqual(req['success'], True)
        
