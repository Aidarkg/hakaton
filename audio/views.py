from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from moviepy.editor import VideoFileClip
import requests
import os


class RecordSpeechAPIView(APIView):
    def post(self, request):
        url = 'https://asr.ulut.kg/api/receive_data'
        token = config('TOKEN')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']
            
            try:
                response = requests.post(url, files={'audio': audio_file}, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({"ошибка": "Не удалось обработать звук"}, status=response.status_code)
            except Exception as e:
                return Response({'Ошибка': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif 'video' in request.FILES:
            video_file = request.FILES['video']
            video_filename = request.FILES['video'].name
            video_file_path = 'media/' + video_filename
            with open(f'{video_file_path}', 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            clip = VideoFileClip(video_file_path)
            audio_file = clip.audio
            video_filename = video_filename.split('.')[0]
            audio_filename = f'media/{video_filename}.mp3'
            audio_file.write_audiofile(audio_filename)
            
            try:
                with open(audio_filename, 'rb') as audio_data:
                    response = requests.post(url, files={'audio': audio_data}, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        return Response({"ошибка": "Не удалось обработать звук"}, status=response.status_code)
            except Exception as e:
                return Response({'Ошибка': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                clip.close()
                audio_file.close()
                os.remove(audio_filename)
                os.remove(video_file_path)