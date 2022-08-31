import datetime
import json
import pytz

# Dependecies
from rest_framework.test import APITestCase
from django.contrib.sessions.models import Session
from authentication.tests import test_features

# Tools
from django.utils import timezone
from core import tools

# Models
from core.models import *


class ReserveTest(APITestCase):
    @staticmethod
    def create_room():
        # create room
        room = SessionRoom(
            title='demo',
            capacity=10,
        )
        room.save()
        
        return room
    
    @staticmethod
    def create_reserve():
        # fetching data
        user = test_features.LoginTest.create_temp_user()
        
        # create room
        room = SessionRoom(
            title='demo',
            capacity=10,
        )
        room.save()
        
        # time stuff
        current_time = timezone.now()
        end_datetime = current_time + datetime.timedelta(hours=2)
        
        reserve = Reserve(
            title='demo',
            reservatore=user,
            room=room,
            duration=2,
            execute_datetime=current_time,
            end_datetime=end_datetime
        )
        reserve.save()
        
        data = {
            'reserve':reserve,
            'user':user
        }
        
        return data
    
    def test_create_reserve(self):
        user = test_features.LoginTest.create_temp_user()
        room = self.create_room()
        
        # login
        token   = test_features.LoginTest.get_token(user)
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        # time stuff
        current_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
        current_datetime = (current_datetime).replace(
            hour=14, minute=30, second=0, microsecond=0)
        start_datetime   = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        end_datetime = current_datetime + datetime.timedelta(hours=2)
        end_datetime = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        
        session = [{
            'title': 'demo',
            'start': start_datetime,
            'end': end_datetime,
        },]
        raw_data = json.dumps(session, indent=4, sort_keys=True, default=str)

        # shaping request
        payload = {
            'session': raw_data,
            'room': room.id
        }
        
        url = '/core/reserve/'
        req = self.client.post(url, payload, **auth_headers).json()
        
        # test
        self.assertTrue(req['success'])
        
    # test case, for each validation err

    def test_user_reserve_list(self):
        # fetching
        data = self.create_reserve()
        
        # login
        user = data['user']
        token = test_features.LoginTest.get_token(user)
        
        # shaping request
        url = '/core/reserve/'
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.get(url, **auth_headers).json()
        
        # test
        self.assertEqual(len(req), 1)
        

    def test_delete_reserve_by_user(self):
        # Fetching data
        data = self.create_reserve()
        reserve = data['reserve']
        token   = test_features.LoginTest.get_token(data['user'])
        
        # shaping request
        url = '/core/reserve/?pk={}'.format(reserve.id)
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.delete(url, **auth_headers).json()
        
        self.assertTrue(req['success'])
       
    def test_delete_reserve_by_user_access_denied(self):
        # build reserve
        data = self.create_reserve()
        reserve = data['reserve']
        
        # another user
        no_access_user = test_features.LoginTest.create_temp_user()
        token   = test_features.LoginTest.get_token(no_access_user)
        
        # shaping request
        url = '/core/reserve/?pk={}'.format(reserve.id)
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.delete(url, **auth_headers)
        req_json = req.json()
        
        self.assertFalse(req_json['success'])
        self.assertEqual(req.status_code, 403)
    
    def test_admin_reserves_list(self):
        # build reserve
        data = self.create_reserve()
        reserve = data['reserve']
        
        # admin user
        admin = test_features.AdminOperationsTest.create_admin_model()
        token = test_features.LoginTest.get_token(admin)
        
        # shaping request
        url = '/core/a_reserves/?pk={}'.format(reserve.id)
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.delete(url, **auth_headers).json()

        self.assertNotEqual(len(req), 0)

    def test_delete_reserve_by_admin(self):
        # build reserve
        data = self.create_reserve()
        reserve = data['reserve']
        
        # admin user
        admin = test_features.AdminOperationsTest.create_admin_model()
        token = test_features.LoginTest.get_token(admin)
        
        # shaping request
        url = '/core/a_reserves/?pk={}'.format(reserve.id)
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.delete(url, **auth_headers).json()

        self.assertTrue(req['success'])

class RoomsTest(APITestCase):  
    @staticmethod
    def create_room():
        # create room
        room = SessionRoom(
            title='demo',
            capacity=10,
        )
        room.save()
        
        return room
        
    def test_rooms_list(self):
        # fetching
        room = self.create_room()
        
        # login
        user = test_features.LoginTest.create_temp_user()
        token   = test_features.LoginTest.get_token(user)
        
        # shaping request
        url = '/core/room/'
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.get(url, **auth_headers).json()
        
        # test
        self.assertEqual(len(req), 1)
        
    def test_room_detail(self):
        # fetching
        room = self.create_room()
        
        # login
        user = test_features.LoginTest.create_temp_user()
        token   = test_features.LoginTest.get_token(user)
        
        # shaping request
        url = '/core/room/'
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        
        req = self.client.get(url, **auth_headers)
        req_json = req.json()
        
        # test
        self.assertEqual(req.status_code, 200)
        
        
        