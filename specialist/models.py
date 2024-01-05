from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Specialist(models.Model):
    user = models.ForeignKey(User, null=True, related_name='specialist', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=20)
    fee = models.IntegerField(default=0)
    image = models.ImageField(upload_to="specialists/images/", null=True, blank=True)
    description=models.TextField(blank=True, default="")
    nmc_num = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=50,default='', blank=True)
    email = models.EmailField(default='', blank=True)
    qualification = models.CharField(max_length=50,default='')
    speciality = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.name} {self.first_name} {self.last_name}'

class Rating(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(default=5)
    def __str__(self):
        return f'{self.specialist.__str__()} rating'
    
class WorkHours(models.Model):
    doctor = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name="work_hours")
    monday = models.TimeField(null=True, blank=True)
    tuesday = models.TimeField(null=True, blank=True)
    wednesday = models.TimeField(null=True, blank=True)
    thursday = models.TimeField(null=True, blank=True)
    friday = models.TimeField(null=True, blank=True)
    saturday = models.TimeField(null=True, blank=True)
    sunday = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.doctor.name}\'s work hours"


class Symptoms(models.Model):
    sym_name=models.CharField(max_length=30)
    def __str__(self):
        return self.sym_name