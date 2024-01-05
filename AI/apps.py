from django.apps import AppConfig
from django.conf import settings

import os
import pickle

class AiConfig(AppConfig):
    name = 'AI'

    path = os.path.join(settings.MODELS,'models.p')

    with open(path,'rb') as pickled:
        model = pickle.load(pickled)
