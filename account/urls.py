from django.contrib import admin
from django.urls import path, include
from . import views
from .views import AccountView

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
]