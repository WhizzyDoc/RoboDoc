from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'nmc_num', 'speciality']
    list_filter = ['speciality']
    list_editable = ['speciality']

admin.site.register(WorkHours)
admin.site.register(Symptoms)
admin.site.register(Category)
admin.site.register(Rating)