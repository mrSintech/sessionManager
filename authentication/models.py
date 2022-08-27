from django.db import models

# Tools
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    username = models.CharField(
        max_length = 50, 
        blank = True, 
        null = True, 
        unique = True
    )
    
    email    = models.EmailField(blank=True, null=True, unique = True)
    phone_no = models.OneToOneField(
        'authentication.UserPhoneNumber',
        on_delete=models.CASCADE,
        related_name='user',
    )
    
    departman = models.ForeignKey(
        'authentication.Departman', 
        on_delete = models.PROTECT,
        related_name= 'users'
    )
    
    def __str__(self):
        return "{} - {} {}".format(self.id, self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        self.username = self.phone_no.number
        super(User, self).save(*args, **kwargs)
 
class Admin(models.Model):
    user = models.OneToOneField(
        'authentication.User',                 
        on_delete=models.CASCADE,
        related_name='admin'
    )
    
    permissions = models.CharField(max_length=255, default='demo')

    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {}".format(self.id, self.user.username)

class Departman(models.Model):
    title       = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {}".format(self.id, self.title)
    

class UserPhoneNumber(models.Model):    
    country_code = models.CharField(max_length=4, default='+98')
    number       = models.CharField(max_length=10, unique=True, db_index=True)
    
    def __str__(self):
        return "{} - {} {} {}".format(
            self.id, 
            self.number,
            self.user.first_name,
            self.user.last_name,
        )
    
    
