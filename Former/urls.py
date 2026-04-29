
from django.contrib import admin
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from Former import views

app_name = 'Former'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/' , views.login , name ='login' ),
    path('logout/' , views.logout , name = 'logout'),

    path('users/' , views.users , name='users'),


    path('users/' , views.users , name='users'),
    path('user_view/<int:id>/' , views.user_view , name='user_view'),
    path('update_user/<int:id>/' , views.edit_user , name='update_user'),
    path('delete_user/<int:id>/' , views.delete_user , name='delete_user'),
    path('new_user/', views.new_user, name='new_user'),
    


        
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
