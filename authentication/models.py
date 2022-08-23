from django.db import models

# Tools
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Dependencies

class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    username        = models.CharField(
        max_length = 50, 
        blank = True, 
        null = True, 
        unique = True
    )
    email    = models.EmailField(unique = True)
    phone_no = models.OneToOneField(
        "authentication.UserPhoneNumber",
        on_delete=models.PROTECT,
        related_name='user',
    )
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    

class UserPhoneNumber(models.Model):    
    country_code = models.CharField(max_length=4)
    number = models.CharField(max_length=10, db_index=True)
    
    def __str__(self):
        return "{}".format(self.number)
    
    
