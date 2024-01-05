from django.urls import path
from .views import *


urlpatterns = [
    path('profile/', ProfileView, name='user_profile'),
    path('login/', LoginView, name='user_login'),
    path('logout/', LogoutView, name='user_logout'),
    path('register/', register, name='user_register'),
    path('specialists/', specialist_list, name='specialists'),
    path('specialists/search/',search_specialist,name='search_specialist'),
    path('specialists/category/<slug:slug>/', category_specialist_list, name='specialists_category'),
    path('specialists/<int:id>/',specialist_detail,name='specialist_detail'),
    path('appointments/',appointments,name='user_appointments'),
    path('appointments/<int:id>/',appointment_detail,name='user_appointment'),
    path('book_appointment/<int:id>/',book_appointment,name='book_appointment'),
]