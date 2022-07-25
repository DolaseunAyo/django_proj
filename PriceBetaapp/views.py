from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, request
from django.contrib import messages
from PriceBetaproject import settings
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')#test for differences in users
def index(request):
	return render(request, "index.html")


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None: #if user decides not to upload a picture
            image = user_profile.profileimg #default profile image set in models.py. which is in the media folder
            location = request.POST('location')

            user_profile.profileimg = image
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None: #on ocassion of upload,all pictures will be saved in the media folder
            image = request.FILES.get('image')
            location = request.POST('location')

            user_profile.profileimg = image
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})


def signup(request):

    if request.method == 'POST':
        email = request.POST('email')
        first_name = request.POST('first_name')
        last_name = request.POST('st_name')
        password = request.POST('password')
        password2 = request.POST('password2')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist')
                return redirect('signup')
            else:
                user = User.objects.create_user(email=email, password=password)
                user.save()

                #login user and direct to profile settings page
                user_login = auth.authenticate(email=email, password=password)
                auth.login(request, user_login)
            

                #profile for new user
                user_model = User.objects.get(email=email)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password do not match')
            return redirect('signup')
    else:
	    return render(request, 'signup.html')


def signin(request):
    
    if request.method == 'POST':
        email = request.POST('email')
        password = request.POST('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Information provided')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')#test for differences in users
def signout(request):
    auth.logout(request)
    return redirect('signin')