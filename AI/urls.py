from django.urls import path
from .views import call_model


urlpatterns = [
    path('',call_model.as_view()),
    # path('doctor',consult)
]