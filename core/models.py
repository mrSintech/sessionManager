from django.db import models

# tools
from django.core.validators import MaxValueValidator

class Reserve(models.Model):
    # Reserve Control
    is_done = models.BooleanField(default=False)
    
    reservatore = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='reserves' 
    )
    
    room = models.ForeignKey(
        'core.SessionRoom',
        on_delete=models.PROTECT,
        related_name='reserves'
    )
    
    # time
    duration = models.IntegerField( # session duration in hours
        validators = [
            MaxValueValidator(4)
        ]
    )
    execute_datetime = models.DateTimeField()
    
    def __str__(self):
        return "{} | {}".format(self.execute_datetime, self.reservatore.first_name, self.reservatore.first_name)
    
class SessionRoom(models.Model):
    """
        Physical session room data
    """
    # room control
    is_active   = models.BooleanField(default=True)
    
    title       = models.CharField(max_length=256)
    
    # Fetures
    has_heater = models.BooleanField(default=False)
    has_cooler = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

