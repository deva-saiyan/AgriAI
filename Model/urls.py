
from django.contrib import admin
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from Model import views

app_name = 'Model'

urlpatterns = [
    path('crop_prediction', views.crop_prediction, name='crop_prediction'),
    


        
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
