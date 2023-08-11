from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def index (request):
    return render(request,"index.html")

def signin (request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(username)
        print(password)

        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)

            return render(request,'index.html')
        else:
            messages.info(request,'Invalid credation')

            return redirect('signin')

    else:
        return render(request,'signin.html')


def signup (request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

         
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken!')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken!')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
            
        else:
            messages.info(request, 'Password do not match!')

            return redirect('signup')

    return render(request,"signup.html")

def profile (request):
    return render(request,"profile.html")

def setting (request):
    return render(request,'setting.html')