import speech_recognition as sr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RecordSpeechAPIView(APIView):
    def post(self, request):
        recognizer = sr.Recognizer()
        
        try:
            # Получаем аудиофайл из запроса
            audio_data = request.FILES['audio_file']
            with sr.AudioFile(audio_data) as source:
                audio = recognizer.record(source)

            # Распознаем речь с помощью Google Speech Recognition
            text = recognizer.recognize_google(audio, language="ru-RU")
            return Response({"text": text}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)
        except sr.UnknownValueError:
            return Response({"error": "Unable to recognize speech"}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
            return Response({"error": "Speech recognition service request failed: {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
