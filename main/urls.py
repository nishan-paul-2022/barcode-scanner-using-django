from django.urls import path
from . import views

urlpatterns = [
    path('', views.views_main, name='main'),
    path('generate_image', views.views_generate_image, name='generate_image'),
    path('detect_from_camera', views.views_detect_from_camera, name='detect_from_camera'),
    path('detect_from_image', views.views_detect_from_image, name='detect_from_image'),
]