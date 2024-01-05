from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import  *
from specialist.models import Category
import json
import re
import csv

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

# Create your views here.
def home(request):
    return render(request, 'index.html')

def create_cat(request):
    ss = []
    cat = Category.objects.all()
    for a in cat:
        ss.append(a.slug)
    cats = ['ENT Specialist', "Orthopedist", "Neurologist", "Immunologist", "Urologist",
            "Dermatologist", "Gastroenterologist", "General Surgeon", "Speech Therapist",
            "Psychiatrist", "Ophthalmologist", "Oncologist", "Neurosurgeon", "Nephrologist",
            "Lymphologist", "Hematologist", "Gynaecologist", "Physician", "Dietician", "Hepatologist",
            "Dentist", "General Physician"]
    for c in cats:
        s = slugify(c)
        if s not in ss:
            Category.objects.create(name=c, slug=s)
        else:
            pass
    return JsonResponse({'status': 'success'})

def create_symptom_model(request):
    s = Symptom.objects.all()
    ss = []
    for a in s:
        ss.append(a.slug)
    texts = []
    symptoms=[]
    with open('new.csv', 'r') as csvfile:
        readline=csvfile.readlines()

        for line in readline:
            linesplit=line.split(',')[1]
            if linesplit!='Symptom':
                texts.append(linesplit)
            for one in texts:
                if one not in symptoms:
                    symptoms.append(one)
    csvfile.close()
    for y in symptoms:
        if slugify(y) not in ss:
            Symptom.objects.create(name=y, slug=slugify(y))
        else:
            pass
    return JsonResponse({'status': 'success'})

def create_disease_model(request):
    s = Disease.objects.all()
    ss = []
    for a in s:
        ss.append(a.slug)
    disease=[]
    diseaseselect=[]
    with open('new.csv', 'r') as csvdisease:
        readline = csvdisease.readlines()
        for line in readline:
            linesplitdisease = line.split(',')[2]
            if linesplitdisease!='Disease':
                disease.append(linesplitdisease)
            for i in disease:
                if i not in diseaseselect:
                    diseaseselect.append(i)

    csvdisease.close()
    for y in diseaseselect:
        if slugify(y) not in ss:
            Disease.objects.create(name=y, slug=slugify(y))
        else:
            pass
    return JsonResponse({'status': 'success'})
    
def add_disease_symptom(request):
    symptoms=[]
    with open('new.csv', 'r') as csvfile:
        readline=csvfile.readlines()

        for line in readline:
            linesplit=line.split(',')[1]
            if linesplit!='Symptom':
                symptoms.append(linesplit)
    csvfile.close()
    
    diseases=[]
    with open('new.csv', 'r') as csvdisease:
        readline = csvdisease.readlines()
        for line in readline:
            linesplitdisease = line.split(',')[2]
            if linesplitdisease!='Disease':
                diseases.append(linesplitdisease)
    csvdisease.close()
    
    for s in range(len(symptoms)):
        d = None
        sy = None
        try:
            d = Disease.objects.get(slug=slugify(diseases[s]))
        except Disease.DoesNotExist:
            d = Disease(name=diseases[s], slug=slugify(diseases[s]))
            d.save()
        try:
            sy = Symptom.objects.get(slug=slugify(symptoms[s]))
        except Symptom.DoesNotExist:
            sy = Symptom(name=symptoms[s], slug=slugify(symptoms[s]))
            sy.save()
        if sy not in d.symptoms.all():
            d.symptoms.add(sy)
            d.save()
        print(f"completed: {int((s/len(symptoms))*100)}%")
    return JsonResponse({'status': 'success'})

def add_disease_specialist(request):
    dd = Disease.objects.all()
    Allergist_Immunologist = ['Allergy', 'Pneumonia', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue',
                                      'Typhoid']
    Cardiologist = ['Hypertension', 'tricuspid valve insufficiency', 'mitral valve insufficiency',
                            'cardiomyopathy', 'myocardial infarction(heartattack)', 'coronary heart disease',
                            'coronary arteriosclerosis', 'sinus tachycardia ', 'aortic valve stenosis',  'pericardial effusion', 'effusion pericardial', 'Endocarditis', 'congestive heart failure ',
                            'failure heart congestive',  'hypertensive disease']
    Dentist = ['Oralcandidiasis']
    Dermatologist = ['carcinoma', 'cellulitis', 'Exanthema']
    Dietician = ['obesity morbid', 'Obesity']
    ENT_specialist  = ["upper respiratory infection", "deglutition disorder"]
    Gastroenterologist  = ['cirrhosis', 'colitis', 'Diverticulitis',
                                                                'Hepatitis', 'hepatitis B', 'hepatitis C']
    Hepatologist=['cirrhosis', 'colitis', 'Diverticulitis',
                                                                 'Diverticulosis', 'Gastritis', 'gastroenteritis',
                                                                 'gastroesophageal reflux disease', 'cirrhosis',
                                                                 'Hepatitis', 'hepatitis B', 'hepatitis C']
    Physician = ["HIV", "acquired immuno-deficiency syndrome", "Hypoglycemia",
                         "Degenerative polyarthritis", "Diabetes", "Hyperlipidemia", "Hyperglycemia",
                         "Hypercholesterolemia", "Hyperbilirubinemia",  "hiv infections",  "ischemia","ketoacidosis diabetic", "peripheral vascular disease"]
    Gynaecologist = ['fibroid tumor']
    Hematologist = ['anemia', 'Thrombocytopaenia', 'sickle cell anemia', 'Pancytopenia', 'bacteremia']
    Lymphologist = ['lymphatic diseases', 'Lymphoma']
    Nephrologist = ['chronic kidney failure', 'failure kidney', 'insufficiency renal', 'kidney disease',
                             'acute kidney failure ', 'pyelonephritis']
    Neurologist = ["Alzheimer's disease", "accident cerebrovascular" ,"Paranoia","Neuropathy",
                           "Delirium","delusion","dementia","Encephalopathy","Epilepsy","parkinson disease",
                           "Schizophrenia","tonic - clonic epilepsy","transient ischemic attack","tonic - clonic seizures"]
    Neurosurgeon = ["Cerebrovascular accident", "Hemiparesis"]
    Oncologist = ['melanoma', 'adenocarcinoma', 'carcinoma breast', 'carcinoma colon', 'carcinoma of lung', 'carcinoma prostate', 'malignant tumor of colon', 'Malignant\xa0neoplasms', 'Neoplasm', 'primary carcinoma of the liver cells', 'malignant neoplasm of prostate', 'malignant neoplasm of lung', 'malignant neoplasm of breast', 'neoplasm metastasis']
    Ophthalmologist = ['Glaucoma']
    Orthopedist = ['arthritis', 'Osteoporosis']
    Psychiatrist = ["affect labile", "anxiety state", "chronic alcoholic","bipolar disorder", "intoxication(alcoholic intoxication)", "Dependence",
                            "depression mental"," depressive disorder","suicide attempt","confusion", "personality disorder", "psychotic disorder"]
    Speechtherapist = ["aphasia",]

    Pulmonologist = ["Pneumocystis carini  pneumonia", "asthma", "bronchitis","carcinoma of lung", "edema pulmonary", "embolism pulmonary"
                             "emphysema pulmonary",  "chronic obstructive airway disease","hypertension pulmonary", "systemic infection", "spasm bronchial",
                             "Septicemia", "sepsis (invertebrate)", "respiratory failure",  "pneumonia", "aspiration","Paroxysmal dyspnea",  "overload fluid",  "Osteomyelitis",
                             "Neutropenia", "infection", "influenza", "malignant neoplasm of lung"]
    Surgeon = ['adhesion', 'biliary calculus', 'carcinoma colon', 'cholecystitis', 'Hemorrhoids', 'colitis',
                       'malignant tumor of colon', 'deep vein thrombosis', 'Thrombus', 'Hernia', 'Hernia hiatal',
                       'Pancreatitis', 'cholelithiasis', 'decubitus ulcer', 'Pneumothorax']
    Urologist = ['benign prostatic hypertrophy', 'carcinoma prostate', 'malignant neoplasm of prostate',
                         'Incontinence', 'infection urinary tract']

    count = 0
    for d in dd:
        count += 1
        predicted_disease = d.name
        consultdoctor = ""
        try:
            if predicted_disease in Cardiologist:
                consultdoctor = "Cardiologist"
            elif predicted_disease in ENT_specialist:
                consultdoctor = "ENT specialist"
            elif predicted_disease in Orthopedist:
                consultdoctor = "Orthopedist"
            elif predicted_disease in Neurologist:
                consultdoctor = "Neurologist"
            elif predicted_disease in Allergist_Immunologist:
                consultdoctor = "Immunologist"
            elif predicted_disease in Urologist:
                consultdoctor = "Urologist"
            elif predicted_disease in Dermatologist:
                consultdoctor = "Dermatologist"
            elif predicted_disease in Gastroenterologist:
                consultdoctor = "Gastroenterologist"
            elif predicted_disease in Surgeon:
                consultdoctor= "General Surgeon"
            elif predicted_disease in Pulmonologist:
                consultdoctor= "Pulmonologist"
            elif predicted_disease in Speechtherapist:
                consultdoctor = "Speech Therapist"
            elif predicted_disease in Psychiatrist:
                consultdoctor = "Psychiatrist"
            elif predicted_disease in Ophthalmologist:
                consultdoctor = "Ophthalmologist"
            elif predicted_disease in Oncologist:
                consultdoctor = "Oncologist"
            elif predicted_disease in Neurosurgeon:
                consultdoctor = "Neurosurgeon"
            elif predicted_disease in Nephrologist:
                consultdoctor = "Nephrologist"
            elif predicted_disease in Lymphologist :
                consultdoctor = "Lymphologist"
            elif predicted_disease in Hematologist:
                consultdoctor = "Hematologist"
            elif predicted_disease in Gynaecologist:
                consultdoctor = "Gynaecologist"
            elif predicted_disease in Physician:
                consultdoctor = "Physician"
            elif predicted_disease in Dietician :
                consultdoctor = "Dietician"
            elif predicted_disease in Hepatologist:
                consultdoctor = "Hepatologist"
            elif predicted_disease in Dentist:
                consultdoctor = "Dentist"
            else:
                consultdoctor = "General Physician"
            if not d.specialist:
                try:
                    cat = Category.objects.get(slug=slugify(consultdoctor))
                    d.specialist = cat
                    d.save()
                except:
                    cat = Category(name=consultdoctor, slug=slugify(consultdoctor))
                    cat.save()
                    d.specialist = cat
                    d.save()
            else:
                pass
            print(f"completed: {int((count/dd.count())*100)}%")
        except Exception as e:
            print(e)
    print('completed: 100%')
    return JsonResponse({'status': 'success'})

#loading trained_model

import joblib as jb
model = jb.load('models.p')

# Create your views here.
def SearchDisease(request):
    return render(request,'searchdisease.html')

def archive(request):
    dx = Disease.objects.all()
    return render(request, 'disease/archive.html', {
        'dx': dx,
    })

def diagnosis(request):
    texts = Symptom.objects.all()
    symptomslist=[]
    for s in texts:
        symptomslist.append(s.name)
    
    if request.method == 'GET' and request.GET.getlist('symptoms'):
        ## access you data by playing around with the request.POST object
        try:
            psymptoms = []
            psymptoms = request.GET.getlist("symptoms")

            #print(psymptoms)

            """      #main code start from here...
            """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            # binary values of symptom
            #print(inputtest)

            predicted = model.predict(inputtest)
            #print("predicted disease is : ")
            #print(predicted)
            #print(type(predicted))
            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            #print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]


            # consult_doctor codes----------

            #   doctor_specialization = ["Cardiologist","ENT specialist","Orthopedist","Neurologist",
            #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist and Hepatologist",
            #                            "Dentist","Dietician","General  Physician","Gynaecologist","Hematologist","Lymphologist"
            #                            "Nephrologist","Neurosurgeon","Oncologist","Ophthalmologist",,"Psychiatrist"
            #                            "Speech therapist","Pulmonologist"]
            #
            #print('Type of specialist',type(Cardiologist))

            disease = Disease.objects.get(slug=slugify(predicted_disease))
            consultdoctor = disease.specialist.name

            # request.session['doctortype'] = consultdoctor

            user = Profile.objects.get(user=request.user)
            # saving to database.....................
            no_of_symp = len(psymptoms)
            symptomsname = ','.join(psymptoms)
            confidence = confidencescore

            diseaseinfo_new = DiseaseInfo(patient=user, condition=disease, no_of_symp=no_of_symp,
                                          symptoms=symptomsname, confidence=confidence, consultdoctor=consultdoctor)
            diseaseinfo_new.save()

            request.session['diseaseinfo_id'] = diseaseinfo_new.id

            #print("disease record saved sucessfully.............................")

            return JsonResponse({
                'status': 'success',
                'Prediction': predicted_disease ,
                'Probab':confidencescore ,
                "Consult": consultdoctor,
                "slug": slugify(consultdoctor)
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'error',
                'message': 'error while generating diagnosis'
            })
    return render(request, 'disease/diagnosis.html', {
        "list2": texts,
    })