from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from edusd_app.models import Emotion
import os
import environ
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import pandas as pd
import numpy as np
import nltk
import re
import joblib
from nltk.corpus import stopwords
from textblob import Word
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

# Create your views here.
def home(request):
    return render(request, 'home.html')

def saveRecording(request):
    if request.is_ajax():
        if request.method == 'POST':
            audio_speech = request.FILES['audio_recording']
            eObject = Emotion(speech_recording=audio_speech, speech_label=audio_speech.name)
            eObject.save()
            return HttpResponse(audio_speech.name+' has been successfully saved to the database.')

@csrf_exempt
def speechToText(request):
    if request.is_ajax():
        if request.method == 'POST':
            recording_name = request.body.decode('UTF-8')
            recording = Emotion.objects.get(speech_label=recording_name)
            audio_speech = recording.speech_recording
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env = environ.Env
            environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
            authenticator = IAMAuthenticator(env('IBM_WATSON_AUTHENTICATOR'))
            speech_to_text = SpeechToTextV1(authenticator=authenticator)
            speech_to_text.set_service_url(env('IBM_WATSON_SERVICE_URL'))
            speech_recognition_results = speech_to_text.recognize(
                audio=audio_speech,
                content_type='audio/webm;codecs=opus',
                model='en-US_BroadbandModel',
                smart_formatting=True,
                split_transcript_at_phrase_end=True,
                speech_detector_sensitivity=0.5,
                background_audio_suppression=0.5
            ).get_result()
            jsonDumps = json.dumps(speech_recognition_results, indent=2)
            jsonLoads = json.loads(jsonDumps)
            str = ""
            while bool(jsonLoads.get('results')): 
                str = jsonLoads.get('results').pop().get('alternatives').pop().get('transcript')+str[:]
            recording.speech_text = str
            recording.save()
            return HttpResponse(str)

def de_repeat(text):
    pattern = re.compile(r"(.)\1{2,}") 
    return pattern.sub(r"\1\1", text) 

@csrf_exempt
def findEmotions(request):
    if request.is_ajax():
        if request.method == 'POST':
            recording_name = request.body.decode('UTF-8')
            recording = Emotion.objects.get(speech_label=recording_name)
            audio_text = recording.speech_text
            text = pd.DataFrame([audio_text])
            emotiondata = pd.read_csv('machine learning data/Emotion_dataset.csv')
            emotiondata = emotiondata.drop(['unit_id', 'golden', 'unit_state', 'trusted_judgments', 'last_judgment_at', 'emotion_confidence', 
            'emotion_gold', 'id', 'idiom_id'], axis=1)
            emotiondata['sentence'] = emotiondata['sentence'].apply(lambda x: " ".join(x.lower() for x in x.split()))
            emotiondata['emotion'] = emotiondata['emotion'].apply(lambda x: " ".join(x.lower() for x in x.split()))
            emotiondata['sentence'] = emotiondata['sentence'].str.replace('[^\w\s]',' ')
            emotiondata['emotion'] = emotiondata['emotion'].str.replace('[^\w\s]',' ')
            stop = stopwords.words('english')
            emotiondata['sentence'] = emotiondata['sentence'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
            emotiondata['sentence'] = emotiondata['sentence'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
            emotiondata['sentence'] = emotiondata['sentence'].apply(lambda x: " ".join(de_repeat(x) for x in x.split()))
            emotiondata = emotiondata.drop(emotiondata[emotiondata.emotion == 'ambiguous'].index)
            X = emotiondata.sentence.values
            le = preprocessing.LabelEncoder()
            Y = le.fit_transform(emotiondata.emotion.values)
            le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            count_vect = CountVectorizer(analyzer='word') 
            count_vect.fit(emotiondata['sentence']) 
            text[0] = text[0].apply(lambda x: " ".join(x.lower() for x in x.split()))
            text[0] = text[0].str.replace('[^\w\s]',' ')
            stoptext = stopwords.words('english')
            text[0] = text[0].apply(lambda x: " ".join(x for x in x.split() if x not in stoptext))
            text[0] = text[0].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
            text_count = count_vect.transform(text[0])
            MultinomialNaiveBayes = joblib.load('machine learning models/MNB.model')
            RandomForestClassifier = joblib.load('machine learning models/RFC.model')
            SupportVectorClassifier = joblib.load('machine learning models/SVC.model')
            pred = le.inverse_transform(RandomForestClassifier.predict(text_count))
            result = ""
            result = ' , '.join(pred)
            emotions = result.capitalize()
            recording.speech_emotions = emotions
            recording.save()
            return HttpResponse(emotions)

def recordings(request):
    eObject = Emotion.objects.all()
    return render(request, 'recordings.html', {'eObj': eObject})