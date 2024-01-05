from django.urls import path
from .views import *
urlpatterns=[
    path('',home,name='home'),
    #path('disease/',SearchDisease,name='disease'),
    path('diagnosis/',diagnosis,name='diagnosis'),
    path('archive/',archive,name='archive'),
    path('create_cat/',create_cat,name='create_cat'),
    path('create_disease/',create_disease_model,name='create_disease'),
    path('create_symptom/',create_symptom_model,name='create_symptom'),
    path('add_symptom/',add_disease_symptom,name='add_symptom'),
    path('add_specialist/',add_disease_specialist,name='add_specialist'),
]
