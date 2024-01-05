from django.shortcuts import render

from .apps import AiConfig

from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings

import os
import numpy as np

import pandas as pd 
# Create your views here.

def make_data(sample):
    path = os.path.join(settings.MODELS,'data/all_x.csv')

    X = pd.read_csv(path)
    total_columns = X.columns
    disease_idx={}
    for i,dis in enumerate(total_columns):
        disease_idx[dis] = i

    data = np.zeros((len(disease_idx),))

    for i in sample:
        data[disease_idx[i]] =1
    return data

class call_model(APIView):
    consultdoctor=''
    def  get(self,request):

        if request.method == 'GET':
            diseaselist = request.GET.getlist('diseaselist')
            #print(diseaselist)

            data = make_data(diseaselist).reshape(1,-1)
            #print(data)
            result = AiConfig.model.predict_proba(data)[0]
            out=dict(zip(AiConfig.model.classes_,result))
            sort_orders = sorted(out.items(), key=lambda x: x[1], reverse=True)
            disease=sort_orders[0]
            differential=sort_orders[1]

            Allergist_Immunologist = ['Allergy', 'Pneumonia', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue',
                                      'Typhoid']

            Cardiologist = ['Hypertension', 'tricuspid valve insufficiency', 'mitral valve insufficiency',
                            'cardiomyopathy', 'myocardial infarction', 'myocardial infarction(heartattack)', 'coronary heart disease',
                            'coronary arteriosclerosis', 'sinus tachycardia ', 'aortic valve stenosis',
                            'pericardial effusion', 'effusion pericardial', 'Endocarditis', 'congestive heart failure ',
                            'failure heart congestive', 'hypertensive disease']
            Dentist = ['Oralcandidiasis']
            Dermatologist = ['carcinoma', 'cellulitis', 'Exanthema']
            Dietician = ['obesity morbid', 'Obesity']
            ENT_specialist = ["upper respiratory infection", "deglutition disorder"]
            Gastroenterologist = ['cirrhosis', 'colitis', 'Diverticulitis',
                                  'Diverticulosis', 'Gastritis', 'gastroenteritis',
                                  'gastroesophageal reflux disease', 'cirrhosis',
                                  'Hepatitis', 'hepatitis B', 'hepatitis C']
            Hepatologist = ['cirrhosis', 'colitis', 'Diverticulitis',
                            'Diverticulosis', 'Gastritis', 'gastroenteritis',
                            'gastroesophageal reflux disease', 'cirrhosis',
                            'Hepatitis', 'hepatitis B', 'hepatitis C']
            Physician = ["HIV", "acquired immuno-deficiency syndrome", "Hypoglycemia",
                         "Degenerative polyarthritis", "Diabetes", "Hyperlipidemia", "Hyperglycemia",
                         "Hypercholesterolemia", "Hyperbilirubinemia", "hiv infections", "ischemia",
                         "ketoacidosis diabetic", "peripheral vascular disease"]
            Gynaecologist = ['fibroid tumor']
            Hematologist = ['anemia', 'Thrombocytopaenia', 'sickle cell anemia', 'Pancytopenia', 'bacteremia']

            Lymphologist = ['lymphatic diseases', 'Lymphoma']
            Nephrologist = ['chronic kidney failure', 'failure kidney', 'insufficiency renal', 'kidney disease',
                            'acute kidney failure ', 'pyelonephritis']
            Neurologist = ["Alzheimer's disease", "accident cerebrovascular", "Paranoia", "Neuropathy",
                           "Delirium", "delusion", "dementia", "Encephalopathy", "Epilepsy", "parkinson disease",
                           "Schizophrenia", "tonic - clonic epilepsy", "transient ischemic attack",
                           "tonic - clonic seizures"]

            Neurosurgeon = ["Cerebrovascular accident", "Hemiparesis"]

            Oncologist = ['melanoma', 'adenocarcinoma', 'carcinoma breast', 'carcinoma colon', 'carcinoma of lung',
                          'carcinoma prostate', 'malignant tumor of colon', 'Malignant\xa0neoplasms', 'Neoplasm',
                          'primary carcinoma of the liver cells', 'malignant neoplasm of prostate',
                          'malignant neoplasm of lung', 'malignant neoplasm of breast', 'neoplasm metastasis']
            Ophthalmologist = ['Glaucoma']
            Orthopedist = ['arthritis', 'Osteoporosis']
            Psychiatrist = ["affect labile", "anxiety state", "chronic alcoholic", "bipolar disorder",
                            "intoxication(alcoholic intoxication)", "Dependence",
                            "depression mental", " depressive disorder", "suicide attempt", "confusion",
                            "personality disorder", "psychotic disorder"]

            SpeechTherapist = ["aphasia", ]

            Pulmonologist = ["Pneumocystis carini  pneumonia", "asthma", "bronchitis", "carcinoma of lung",
                             "edema pulmonary", "embolism pulmonary"
                                                "emphysema pulmonary", "chronic obstructive airway disease",
                             "hypertension pulmonary", "systemic infection", "spasm bronchial",
                             "Septicemia", "sepsis (invertebrate)", "respiratory failure", "pneumonia", "aspiration",
                             "Paroxysmal dyspnea", "overload fluid", "Osteomyelitis",
                             "Neutropenia", "infection", "influenza", "malignant neoplasm of lung"]

            Surgeon = ['adhesion', 'biliary calculus', 'carcinoma colon', 'cholecystitis', 'Hemorrhoids', 'colitis',
                       'malignant tumor of colon', 'deep vein thrombosis', 'Thrombus', 'Hernia', 'Hernia hiatal',
                       'Pancreatitis', 'cholelithiasis', 'decubitus ulcer', 'Pneumothorax']
            Urologist = ['benign prostatic hypertrophy', 'carcinoma prostate', 'malignant neoplasm of prostate',
                         'Incontinence', 'infection urinary tract']

            print('Type of specialist', type(Cardiologist))
            consultdoctor=''
            if disease[0] in Cardiologist:

                consultdoctor = "Cardiologist"


            elif disease[0] in ENT_specialist:

                consultdoctor = "ENT specialist"

            elif disease[0] in Orthopedist:

                consultdoctor = "Orthopedist"

            elif disease[0] in Neurologist:

                consultdoctor = "Neurologist"

            elif disease[0] in Allergist_Immunologist:

                consultdoctor = "Allergist/Immunologist"

            elif disease[0] in Urologist:

                consultdoctor = "Urologist"

            elif disease[0] in Dermatologist:

                consultdoctor = "Dermatologist"

            elif disease[0] in Gastroenterologist:

                consultdoctor = "Gastroenterologist"

            elif disease[0] in Surgeon:

                consultdoctor = "Surgeon"

            elif disease[0] in Pulmonologist:

                consultdoctor = "Pulmonologist"

            elif disease[0] in SpeechTherapist:

                consultdoctor = "Speech Therapist"

            elif disease[0] in Psychiatrist:

                consultdoctor = "Psychiatrist"

            elif disease[0] in Ophthalmologist:

                consultdoctor = "Ophthalmologist"

            elif disease[0] in Oncologist:

                consultdoctor = "Oncologist"

            elif disease[0] in Neurosurgeon:

                consultdoctor = "Neurosurgeon"

            elif disease[0] in Nephrologist:

                consultdoctor = "Nephrologist"

            elif disease[0] in Lymphologist:

                consultdoctor = "Lymphologist "

            elif disease[0] in Hematologist:

                consultdoctor = "Hematologist"

            elif disease[0] in Gynaecologist:

                consultdoctor = "Gynaecologist"

            elif disease[0] in Physician:

                consultdoctor = "Physician"

            elif disease[0] in Dietician:

                consultdoctor = "Dietician "

            elif disease[0] in Hepatologist:

                consultdoctor = "Hepatologist"

            elif disease[0] in Dentist:

                consultdoctor = "Dentist"

            else:

                consultdoctor = "General Physician"

            response = {"Prediction":disease[0],
                        "Differential": differential[0],
                        'Probab':disease[1],
                        'diff_prob': differential[1],
                        'Consult':consultdoctor}


            print(response)
            return JsonResponse(response)

# def consult(request):
#     query = request.GET['resultSpecialist']
#     print(query)
#     if len(query) > 85:
#         speciality = []
#     else:
#         Sname = doctor_profile.objects.filter(name__icontains=query)
#         Sdesc = doctor_profile.objects.filter(desc__icontains=query)
#         speciality = Sname.union(Sdesc)
#     if speciality.count() == 0:
#         messages.error(request, 'No Search result found. Please refine your query')
#
#     params = {'speciality': speciality, 'query': query}
#     return render(request, 'search.html', params)


