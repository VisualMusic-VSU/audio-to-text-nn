import uuid

from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from faster_whisper import WhisperModel
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TranscribeAudio(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=None,
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, description='Аудио для расшифровки', type=openapi.TYPE_FILE),
        ],
        responses={
            200: openapi.Response(
                description="Расшифровка прошла успешно",
            ),
            400: openapi.Response(
                description="Ошибки в запросе",
            ),
        }
    )
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        audio_file = request.FILES['file']

        # Генерация уникального имени
        unique_name = f"{uuid.uuid4()}"
        file_path = default_storage.save(f"uploads/{unique_name}", audio_file)
        full_path = default_storage.path(file_path)

        try:
            model = WhisperModel("base", device="cuda")
            segments, _ = model.transcribe(full_path)

            transcript = [segment.text.strip() for segment in segments]
            return Response({"lyrics": transcript})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            # Удаляем файл независимо от результата
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
