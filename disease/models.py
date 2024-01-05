from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from specialist.models import *
from tinymce.models import HTMLField
#from django.contrib.postgres.fields import ArrayField

class Symptom(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meaning = models.TextField(blank=True)
    image = models.ImageField(upload_to="symptoms/", null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Disease(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meaning = HTMLField(blank=True)
    image = models.ImageField(upload_to="diseases/", null=True, blank=True)
    specialist = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="diseases_specialized")
    symptoms = models.ManyToManyField(Symptom, blank=True, related_name="related_diseases")
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class DiseaseInfo(models.Model):
    patient = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    condition = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, related_name="disease_diagnosed")
    no_of_symp = models.IntegerField()
    #symptomsname = ArrayField(models.CharField(max_length=200))
    symptoms = models.CharField(max_length=2000)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200)

    def get_symptom_list(self):
        return self.symptoms.split(',')
    
    def __str__(self):
        return f"{self.patient.__str__()} - {self.condition.name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="appointments_booked")
    doctor = models.ForeignKey(Specialist, on_delete=models.SET_NULL, null=True, related_name="appointments_booked")
    ai_diagnosis = models.ForeignKey(DiseaseInfo, on_delete=models.SET_NULL, null=True, related_name="appointments")
    complaint = models.TextField(blank=True)
    symptoms = models.CharField(max_length=2000)
    doctor_diagnosis = models.CharField(max_length=255, blank=True)
    doctor_note = HTMLField()
    prescription = HTMLField()
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    confirmed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(default=5)
    def __str__(self):
        return f'{self.doctor.name} {self.doctor.first_name} {self.doctor.last_name} - {self.patient.__str__()}'
    class Meta:
        ordering = ['-date', '-time']
    def get_symptom_list(self):
        return self.symptoms.split(',')
