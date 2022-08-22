from django.urls import path, include

# Rest Framework
from rest_framework import routers

# Views
from . import views

router = routers.DefaultRouter()

router.register('test', views.Test, 'test')

router.register('login', views.UserLogin, 'login')

app_name = 'auth_api'
urlpatterns = [
    path('', include(router.urls)),
]