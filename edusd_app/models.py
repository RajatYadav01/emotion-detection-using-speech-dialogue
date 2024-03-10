from django.db import models

# Create your models here.
class Emotion (models.Model):
    speech_label = models.CharField(max_length=100, blank=True, null=True)
    speech_recording = models.FileField(upload_to='edusd/')
    speech_text = models.TextField()
    speech_emotions = models.TextField()

    def __str__(self):
        self.speech_label
