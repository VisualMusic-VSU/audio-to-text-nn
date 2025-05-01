from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from faster_whisper import WhisperModel

class TranscribeAudio(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        audio_file = request.FILES['file']
        file_path = default_storage.save(f"uploads/{audio_file.name}", audio_file)

        model = WhisperModel("base", device="cpu")
        segments, _ = model.transcribe(default_storage.path(file_path))

        transcript = [segment.text.strip() for segment in segments]

        default_storage.delete(file_path)

        return Response({"transcript": transcript})