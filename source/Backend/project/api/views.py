from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import ImageSerializer
from rest_framework.viewsets import ModelViewSet

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MultipleFileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')

        # Process and save each file
        for uploaded_file in files:
            # Your file handling logic here (validation, saving to storage, etc.)
            # Example: Save file to a specific directory
            with open(f'media/{uploaded_file.name}', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        return Response({'message': 'Files uploaded successfully'}, status=201)