from django.urls import path
from .views import ImageUploadView, MultipleFileUploadView


urlpatterns = [
    path('api/upload_image/', ImageUploadView.as_view(), name='image-upload'),
    path('api/upload_folder/', MultipleFileUploadView.as_view(), name='folder-upload'),
    # path('api/color/', ColorResultView.as_view(), name='color'),
]
                                 