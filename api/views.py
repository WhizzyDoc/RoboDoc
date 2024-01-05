from rest_framework import generics, viewsets
from disease.models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import login, authenticate, logout
import secrets
import re
import json
from django.db.models import Q
from .encrypt_utils import encrypt, decrypt
from datetime import datetime, timedelta
from django.utils import timezone
import random
import decimal
import math
import string

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

# Create your views here.
class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [AllowAny]
    @action(detail=False,
            methods=['get'])
    def get_disease_detail(self, request, *args, **kwargs):
        id = self.request.query_params.get('id')
        try:
            d = Disease.objects.get(id=int(id))
            return Response({
                'status': 'success',
                'message': 'Details fetched sucessfully',
                'data': DiseaseSerializer(d).data
            })
        except:
            return Response({
                'status': 'error',
                'message': 'Disease not found'
            })

