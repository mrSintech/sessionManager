from django.db import models

# Tools
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    """
        main user model
    """
    username        = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email           = models.EmailField(('email address'), unique = True)
    # phone_no        = models.OneToOneField(
    #     "authentication.UserPhoneNumber",
    #     on_delete=models.PROTECT,
    #     related_name='user',
    # )
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    

class UserPhoneNumber(models.Model):
    """"""
    number = PhoneNumberField()
    
    def __str__(self):
        return "{}".format(self.number)
    
    
