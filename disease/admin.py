from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialist']
    list_filter = ['specialist']
    list_editable = ['specialist']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name', 'meaning']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(DiseaseInfo)
admin.site.register(Appointment)
