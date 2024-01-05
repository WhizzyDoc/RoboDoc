
# Create your models here.
#The script is used for creating models for app.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image

class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(default='/images/default.jpg', upload_to='profile_pics', null=True, blank=True)
    age = models.IntegerField(default=0)
    first_name = models.CharField(max_length=100, verbose_name="First Name", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", null=True, blank=True)
    email = models.EmailField(max_length=200, verbose_name="Email", null=True, blank=True)
    phone_number = models.CharField(max_length=200, verbose_name="Phone Number", null=True, blank=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    """
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)    
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    """


class UserReview(models.Model):
    review=models.TextField()

    def __str__(self):
        return self.review
