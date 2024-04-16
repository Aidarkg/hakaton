from django.contrib import admin
from django.urls import path
from audio.views import RecordSpeechAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('record-speech/', RecordSpeechAPIView.as_view(), name='record_speech'),
]
