from django.shortcuts import render , redirect 
from django.http import HttpResponse
from django.contrib import messages

def home (request):
    return render(request , 'home.html')



def about (request):
    return render(request , 'about.html')

def crop_details(request):
    return render(request , 'crop_details.html')

def leaf_details(request):
    return render(request , 'leaf_details.html')

def pest_details(request):
    return render(request , 'pest_details.html')


def contact (request):
    return render(request , 'contact.html')