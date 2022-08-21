from django.db import models

# tools
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class Session(models.Model):
    """
        Main session model hold's crucial main data about session
    """
    # reservatore = 
    duration = models.IntegerField( # session duration in hours
        validators = [
            MaxValueValidator(4)
        ]
    )
    
    def __str__(self):
        return self.id
    
class SessionRoom(models.Model):
    """
        Physical session room data
    """
    # room control
    is_active   = models.BooleanField(default=True)
    
    title       = models.CharField(max_length=256)
    have_heater = models.BooleanField(default=False)
    have_cooler = models.BooleanField(default=False)
    
    
class User(AbstractUser):
    """
        main user model
    """
    username        = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email           = models.EmailField(('email address'), unique = True)
    phone_no        = models.OneToOneField(
        "core.UserPhoneNumber",
        on_delete=models.PROTECT,
        related_name='user',
    )
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
class UserPhoneNumber(models.Model):
    """"""
    number = PhoneNumberField()
    
    def __str__(self):
        return "{}".format(self.number)
    
    
