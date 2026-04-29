
from django.contrib import admin
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from Pest import views

app_name = 'Pest'

urlpatterns = [
    path('pest_prediction', views.pest_prediction, name='pest_prediction'),
        
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





 