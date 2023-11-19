from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageSerializer
from .models import Image
from .color import process_color_dataset
from .texture import process_texture_dataset
import cv2, os, shutil, time




class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        Images = Image.objects.all()
        if Images.exists():
            Images[0].delete()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        Images = Image.objects.all()
        serializer = ImageSerializer(Images, many=True)
        return Response(serializer.data)
    


class MultipleFileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        files = request.FILES.getlist('files')
        shutil.rmtree('media/dataset/')
        os.makedirs('media/dataset/')

        # simpan setiap file
        for uploaded_file in files:
            with open(f'media/dataset/{uploaded_file.name}', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        return Response({'message': 'Files uploaded successfully'}, status=201)
    
    def get(self, request):
        media_directory = 'media/dataset'
        similarity_scores = []
        i = 1
        for filename in os.listdir(media_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                similarity_scores.append({
                    "id": i,  
                    "persentase": 80,  # dummy element
                    "img": filename  
                })
                i = i+1

            

        return Response(similarity_scores, status=200)


class ColorResultView(APIView):
    def get(self, request):
        Images = Image.objects.all()
        # Mengambil objek Image pertama dari queryset
        first_image = Images.first()
        # Mengakses nilai dari atribut 'image' dari objek Image pertama
        image_name = first_image.image.name
        input_image = cv2.imread(f'media/{image_name}')
        dataset_folder = 'media/dataset/'
        t0 = time.time()
        hasil = process_color_dataset(input_image, dataset_folder)
        t1 = time.time()
        exec = t1-t0
        hasil[0]['durasi'] = round(exec,3) # menyimpan excecution time di dictionary durasi di elemen pertama
        return Response(hasil, status=200)
    
class TextureResultView(APIView):
    def get(self, request):
        Images = Image.objects.all()
        input_image = cv2.imread(f'media/{Images.first().image.name}')
        dataset_folder = 'media/dataset/'
        t0 = time.time()
        hasil = process_texture_dataset(input_image, dataset_folder)
        t1 = time.time()
        exec = t1-t0
        hasil[0]['durasi'] = round(exec,3) # menyimpan excecution time di dictionary durasi di elemen pertama
        return Response(hasil, status=200)


