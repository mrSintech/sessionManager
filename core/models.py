from django.db import models

# tools
from django.core.validators import MaxValueValidator

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

