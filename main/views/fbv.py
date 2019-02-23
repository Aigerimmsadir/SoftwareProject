from main.models import Restaurant,RestaurantReview,Dish,DishReview
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from main.serializers import UserModelSerializer
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm

@api_view(['GET','POST'])
@csrf_exempt
def mynewregister(request):
    form = UserCreationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'register.html', {'form': form})

@api_view(['GET','POST'])
@csrf_exempt
def mynewlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            print(request.user)
            print('you logged in')
            return redirect('home')
        else:
            error = "username or password incorrect"
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
@api_view(['GET'])
@csrf_exempt
def current_user(request):
    serializer = UserModelSerializer(request.user)
    return Response(serializer.data)
@api_view(['GET'])
@csrf_exempt
def home(request):
    rests = Restaurant.objects.all()[:4]
    return render(request,"index.html",{'rests':rests})