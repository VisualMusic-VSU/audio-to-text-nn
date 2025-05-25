from django.urls import path
from .views import TranscribeAudio

urlpatterns = [
    path('process/', TranscribeAudio.as_view(), name='transcribe-audio'),
]
