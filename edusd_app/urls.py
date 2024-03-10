from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recordings', views.recordings, name='recordings'),
    path('saveRecording', views.saveRecording, name='saveRecording'),
    path('speechToText', views.speechToText, name='speechToText'),
    path('findEmotions', views.findEmotions, name='findEmotions'),
]