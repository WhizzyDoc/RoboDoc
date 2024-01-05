from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages
from math import ceil
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery
from . import views
from django.views.generic import TemplateView
from django.views.generic import DetailView
# Create your views here.



