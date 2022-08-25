import os
import sys

# Models
from django.db import models

# tools
from django.core.validators import MaxValueValidator

# image process
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Managers
class RoomActiveManager(models.Manager):
    def get_queryset(self):
        return super(RoomActiveManager, self).get_queryset().filter(
            is_active = True
        )

class Reserve(models.Model):
    # Reserve Control
    is_done = models.BooleanField(default=False)
    
    reservatore = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='reserves' 
    )
    
    departman = models.ForeignKey(
        'authentication.Departman', 
        on_delete=models.PROTECT,
        related_name='reserves',
        blank=True,
        null=True
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
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return "{} | {}".format(self.execute_datetime, self.reservatore.first_name, self.reservatore.first_name)
    
    def assign_departman(self):
        departman = self.reservatore.departman
        self.departman = departman
    
    def save(self, *args, **kwargs):
        self.assign_departman()
        super(Reserve, self).save(*args, **kwargs)
    
class SessionRoom(models.Model):
    """
        Physical session room data
    """
    # room control
    is_active   = models.BooleanField(default=True)
    
    title       = models.CharField(max_length=256)
    capacity    = models.IntegerField() # persons
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    objects  = models.Manager()
    actives  = RoomActiveManager()
    
    # pics -> RoomPic
    # info -> RoomInfo
    
    def __str__(self):
        return self.title

class RoomInfo(models.Model):
    room = models.ForeignKey(
        'core.SessionRoom',           
        on_delete=models.CASCADE,
        related_name='info'
    )
    
    key   = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {} - {}".format(self.id, self.key, self.room.title)

# Room Pics
def public_room_pic_path_generator(instance, filename):
    return os.path.join(
        'public/internal/rooms', 
        str(instance.room.id), 
        filename
    )

class RoomPic(models.Model):
    room = models.ForeignKey(
        'core.SessionRoom', 
        on_delete=models.CASCADE,
        related_name='pics'
    )
    pic = models.ImageField(
        upload_to= public_room_pic_path_generator
    )
    pic_thumbnail  = models.ImageField(
        upload_to=public_room_pic_path_generator, 
        blank=True,
        null=True
    )
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.room.title
    
    def resize_pic(self):
        # TODO: Refactor
        if self.pic: 
            try:
                DJANGO_TYPE = self.pic.file.content_type 
                if DJANGO_TYPE == 'image/jpeg':
                    image_temp = Image.open(self.pic)
                    output_IoStream = BytesIO()
                    image_temp_thumbnailed = image_temp.thumbnail((720, 720))
                    image_temp.save(output_IoStream, format='JPEG', quality=100)
                    output_IoStream.seek(0)
                    self.pic = InMemoryUploadedFile(
                        output_IoStream,
                        'ImageField', 
                        "%s.jpeg" % self.pic.name.split('.')[0], 
                        'image/jpeg', 
                        sys.getsizeof(output_IoStream), 
                        None
                    )
                    return True

                elif DJANGO_TYPE == 'image/png':
                    image_temp = Image.open(self.pic)
                    output_IoStream = BytesIO()
                    image_temp_thumbnailed = image_temp.thumbnail((720, 720))
                    image_temp.save(output_IoStream, format='PNG', quality=100)
                    output_IoStream.seek(0)
                    self.pic = InMemoryUploadedFile(
                        output_IoStream,
                        'ImageField', 
                        "%s_thumb.png" % self.pic.name.split('.')[0], 
                        'image/png', 
                        sys.getsizeof(output_IoStream), 
                        None
                    )
            
            except:
                pass
        return True
        
    # Generate thumbnail for room photo
    def make_thumbnail(self):
        if self.pic: 
            try:
                DJANGO_TYPE = self.pic.file.content_type 
                if DJANGO_TYPE == 'image/jpeg':
                    image_temp = Image.open(self.pic)
                    output_IoStream = BytesIO()
                    image_temp_thumbnailed = image_temp.thumbnail((300, 300))
                    image_temp.save(output_IoStream, format='JPEG', quality=100)
                    output_IoStream.seek(0)
                    self.pic_thumbnail = InMemoryUploadedFile(
                        output_IoStream,
                        'ImageField', 
                        "%s_thumb.jpeg" % self.pic.name.split('.')[0], 
                        'image/jpeg', 
                        sys.getsizeof(output_IoStream), 
                        None
                    )
                    return True

                elif DJANGO_TYPE == 'image/png':
                    image_temp = Image.open(self.pic)
                    output_IoStream = BytesIO()
                    image_temp_thumbnailed = image_temp.thumbnail((300, 300))
                    image_temp.save(output_IoStream, format='PNG', quality=100)
                    output_IoStream.seek(0)
                    self.pic_thumbnail = InMemoryUploadedFile(
                        output_IoStream,
                        'ImageField', 
                        "%s_thumb.png" % self.pic.name.split('.')[0], 
                        'image/png', 
                        sys.getsizeof(output_IoStream), 
                        None
                    )
            
            except:
                self.pic_thumbnail = self.pic
                
        return True

    def save(self, *args, **kwargs):
        self.resize_pic()
        self.make_thumbnail()
        super(RoomPic, self).save(*args, **kwargs)
