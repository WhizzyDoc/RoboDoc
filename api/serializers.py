from rest_framework import serializers
from disease.models import *
from django.contrib.auth.models import User

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'name', 'meaning', 'image']

class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    class Meta:
        model = Disease
        fields = ['id', 'name', 'meaning', 'image', 'symptoms']
