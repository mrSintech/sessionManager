from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Session)
admin.site.register(SessionRoom)
admin.site.register(UserPhoneNumber)
