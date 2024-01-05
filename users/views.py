from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
from specialist.models import *
from disease.models import *
import re

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'\d', password):
        return False
    return True

def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9]+$'
    if re.match(pattern, username):
        return True
    else:
        return False

def sterilize(s):
    s = ''.join(letter for letter in s if letter.isalnum())
    return s


@csrf_protect
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        password = request.POST.get('password')
        if not is_valid_email(email):
            messages.warning(request, f'Invalid Email Address')
            return redirect('user_register')
        if not is_valid_username(username):
            messages.warning(request, f'Invalid Username.')
            return redirect('user_register')
        if not is_valid_password(password):
            messages.warning(request, f'Invalid Password combination. Password must be at least 8 characters long and must contain letters and numbers')
            return redirect('user_register')
        new_user = User(username=username, email=email, first_name=fname, last_name=lname)
        new_user.set_password(password)
        new_user.save()
        Profile.objects.create(user=new_user, age=age, gender=gender, email=email, first_name=fname, last_name=lname, phone_number=phone)
        messages.success(request, f'YOUR ACCOUNT HAS BEEN CREATED!YOU ARE ABLE TO LOGIN NOW')
        return redirect('user_login')
    return render(request, 'users/register.html')

@csrf_protect
def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=sterilize(username),
                                password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('user_profile')
            else:
                messages.warning(request, f'Sorry, Your account has been deactivated.')
                return redirect('user_login')
        else:
            messages.warning(request, f'Invalid Login Credentials.')
            return redirect('user_login')
    elif request.method == 'GET':
        if request.user and request.user.is_authenticated:
            return redirect('user_profile')
        return render(request, 'users/login.html')

def LogoutView(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def ProfileView(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        messages.success(request, f'Your profile has been updated successfully')
        return redirect('user_profile')
    else:
        return render(request, 'users/profile.html', {
            'user': request.user,
            'profile': profile
        })

@login_required(login_url='user_login')
def specialist_list(request):
    doctors = Specialist.objects.all()
    cats = Category.objects.all()
    params = {
        'speciality':doctors,
        'cats': cats
        }
    return render(request,'users/doctors.html', params)

@login_required(login_url='user_login')
def category_specialist_list(request, slug):
    category = Category.objects.get(slug=slug)
    cats = Category.objects.all()
    doctors = Specialist.objects.filter(speciality=category)
    params = {
        'speciality':doctors,
        'cats': cats,
        'category': category,
        }
    return render(request,'users/doctors.html', params)

@login_required(login_url='user_login')
def specialist_detail(request, id):
    doctor = Specialist.objects.get(id=id)
    params = {
        'doctor':doctor,
        }
    return render(request,'users/doctor_profile_detail.html', params)

@login_required(login_url='user_login')
def search_specialist(request):
    # query=request.GET['query']
    # speciality=Specialist.objects.filter(desc__icontains=query)
    # params={'speciality':speciality}
    # return render(request,'search.html',params)
    query = request.GET['query']
    cats = Category.objects.all()
    if len(query) > 85:
        speciality = []
    else:
        Sname = Specialist.objects.filter(name__icontains=query)
        Sdesc = Specialist.objects.filter(description__icontains=query)
        speciality = Sname.union(Sdesc)
    if speciality.count() == 0:
        messages.error(request, f'No Search result found for {query}. Please refine your query')
    else:
        messages.success(request, f'Found {speciality.count()} results for \'{query}\'.')
    params = {
        'speciality': speciality,
        'query': query,
        'cats': cats,
        }
    return render(request, 'users/doctors.html', params)

@login_required(login_url='user_login')
def appointments(request):
    profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=profile)
    return render(request, 'users/appointments.html', {
        'profile': profile,
        'appointments': appointments,
    })

@login_required(login_url='user_login')
def appointment_detail(request, id):
    profile = Profile.objects.get(user=request.user)
    appointment = Appointment.objects.get(id=int(id), patient=profile)
    return render(request, 'users/appointment_detail.html', {
        'profile': profile,
        'appointment': appointment,
    })

@login_required(login_url='user_login')
@csrf_exempt
def book_appointment(request, id):
    doctor = Specialist.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    ss = Symptom.objects.all()
    diag_id = None
    diag = None
    if 'diseaseinfo_id' in request.session:
        diag_id = request.session['diseaseinfo_id']
        diag = DiseaseInfo.objects.get(id=int(diag_id))
    if request.method == 'POST':
        try:
            date = request.POST.get('date')
            time = request.POST.get('time')
            complaint = request.POST.get('complaint')
            diag_id = request.session['diseaseinfo_id']
            diag = DiseaseInfo.objects.get(id=int(diag_id))
            new_a = Appointment(patient=profile, doctor=doctor, ai_diagnosis=diag,
                                complaint=complaint, symptoms=diag.symptoms, date=date,
                                time=time)
            new_a.save()
            message = "You have successfully booked an appointment. You will be notified as soon as the appointment is confirmed by the specialist."
            messages.success(request, message)
            return JsonResponse({
                'status': 'success',
                'message': message
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'error',
                'message': "Error occured while booking an appointment."
            })
    params = {
        'doctor':doctor,
        'diagnosis': diag,
        'profile': profile,
        'ss': ss
        }
    return render(request,'users/book_appointment.html', params)
