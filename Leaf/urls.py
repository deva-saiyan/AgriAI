
from django.contrib import admin
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from Leaf import views

app_name = 'Leaf'

urlpatterns = [
    path('leaf_prediction', views.leaf_prediction, name='leaf_prediction'),
        
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





 