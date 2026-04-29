from django.shortcuts import render , redirect 
from django.http import HttpResponse
from django.contrib import messages

def home (request):
    return render(request , 'home.html')



def about (request):
    return render(request , 'about.html')


def contact (request):
    return render(request , 'contact.html')