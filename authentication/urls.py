from django.urls import path, include

# Rest Framework
from rest_framework import routers

# Views
from . import views

router = routers.DefaultRouter()

router.register('login',       views.UserLogin,          'login')
router.register('verify',      views.LoginVerify,        'verify')
router.register('a_login',     views.AdminLogin,         'a-login')
router.register('departments', views.DepartmentViewSet,  'departments')
router.register('add_user',    views.AdminAddUserViewSet,'add_user')

app_name = 'auth_api'
urlpatterns = [
    path('', include(router.urls)),
]