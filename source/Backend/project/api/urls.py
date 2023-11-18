from django.urls import path
from .views import ImageUploadView, MultipleFileUploadView
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('folders', FolderViewSet, basename='folders')

urlpatterns = [
    path('api/upload_image/', ImageUploadView.as_view(), name='image-upload'),
    path('api/upload_folder/', MultipleFileUploadView.as_view(), name='folder-upload'),
    # path('', include(router.urls))
]
                                 