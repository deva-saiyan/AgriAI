from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# Registe Model ----------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = Register_Form(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['date_of_birth']
            photo = form.cleaned_data['photo']

            #  Check if email already exists
            if User.objects.filter(username=name).exists():
                messages.error(request, "Email already registered")
                return redirect('Home:register')

            #  Create Django user
            user = User.objects.create_user(
                username=name,   # email as username
                password=password
            )

            #  Create profile (IMPORTANT FIX)
            Register_Model.objects.create(
                user=user,
                name=name,
                phone=phone,
                gender=gender,
                date_of_birth=dob,
                photo=photo
            )

            messages.success(request, "Registration successful")
            return redirect('Former:login')

    else:
        form = Register_Form()

    return render(request, 'register.html', {'form': form})


# Login ------------------------------------------------------------------------------------


@csrf_exempt
def login(request):
    form = Login_Form()

    if request.method == 'POST':
        form = Login_Form(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']   #  FIX
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=name,   #  email used as username
                password=password
            )

            if user is not None:
                auth_login(request, user)
                return redirect('Home:home')
            else:
                messages.error(request, 'Invalid Email or Password')

    return render(request, 'login.html', {'login_form': form})



# Logout ------------------------------------------------------------------------

def logout(request):
    auth_logout(request)
    return redirect('Former:login')



# Viwe User ----------------------------------------------------------------------------

def users(request):
    data = Register_Model.objects.all()
    return render(request, 'users.html', {
        'register_data': data
    })




# view User ---------------------------------------------------------------------

def user_view(request, id):
    user = get_object_or_404(Register_Model, id=id)
    return render(request, 'user_view.html', {
        'user': user   # MUST be "user"
    })



# Edit User ----------------------------------------------------

def edit_user(request, id):
    user = get_object_or_404(Register_Model, id=id)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.district = request.POST.get("district")
        user.place = request.POST.get("place")

        user.save()
        return redirect('users')

    return render(request, 'user_edit.html', {
        'user': user
    })



# Delete User -------------------------------------------------------------------------

def delete_user(request, id):
    user_data = get_object_or_404(Register_Model, id=id)
    user_data.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('Former:users')


# Search User ----------------------------------------------------------------------
from django.shortcuts import render
from django.db.models import Q
from .models import Register_Model

def users(request):

    query = request.GET.get('q', '')

    register_data = Register_Model.objects.all()

    if query:
        register_data = register_data.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(request, 'users.html', {
        'register_data': register_data,
        'query': query
    })


# -----------------------------------------------------------------------------------------

def new_user(request):
    if request.method == 'POST':
        form = Register_Form(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['date_of_birth']
            photo = form.cleaned_data['photo']

            #  Check if email already exists
            if User.objects.filter(username=name).exists():
                messages.error(request, "Email already registered")
                

            #  Create Django user
            user = User.objects.create_user(
                username=name,   # email as username
                password=password
            )

            #  Create profile (IMPORTANT FIX)
            Register_Model.objects.create(
                user=user,
                name=name,
                phone=phone,
                gender=gender,
                date_of_birth=dob,
                photo=photo
            )

            messages.success(request, "Registration successful")
            return redirect('Former:users')
            

    else:
        form = Register_Form()

    return render(request, 'user_new.html', {'form': form})
