from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.core import serializers


import matplotlib.pyplot as plt
from random import randint as r
import io, urllib, base64,json

from django.shortcuts import render, redirect
from main.forms import UserForm, UserProfileForm

import meraki
from main.models import Organisation
from main.models import Network
from main.models import *

# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the main index.")

    response = render(request, 'main/index.html', context = {'example_text' : 'THIS IS EXAMPLE TEXT',})
    return response


def ben(request):
    return HttpResponse("Ben's page...")


def fraser(request):
    return HttpResponse("Fraser's page...")
    
    
def jake(request):
    dataX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    dataY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    newFig = plt.figure()
    mainAx = newFig.add_subplot(1, 1, 1)
    
    mainAx.scatter(dataX, dataY, color = 'red')
    mainAx.set_xlabel("Test")#
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    
    graphAsPNG = buffer.getvalue()
    buffer.close()
    
    graphAsPNG = base64.b64encode(graphAsPNG)
    graphAsPNG = graphAsPNG.decode('utf-8')
    
    context_dict = {
        'test': graphAsPNG,
        'orgs': Organisation.objects.all()
    }
    
    return render(request, 'main/jakePage.html', context = context_dict)


def showOrg(request, name_slug):
    organisation = Organisation.objects.get(slug=name_slug)
    networks = Network.objects.filter(org = organisation)
    
    context_dict = {
        'org': organisation,
        'net': networks
    }
    
    return render(request, "main/orgPage.html", context = context_dict)


def johnathan(request):
    return HttpResponse("Johnathan's page... Test")


# View for register page
def register(request):
    if request.user:
        return redirect('/profile')
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                 'main/register.html',
                 context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})

def user_login(request):
    if request.user:
        return redirect('/profile')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                #return HttpResponse("Successfully logged in\napikey: " +'example' )
                return redirect('/profile')
                #return redirect(reverse('index'))
            else:
                return HttpResponse("Your Login account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'main/login.html')

@login_required
def profile(request):
    tmpObj = json.loads(serializers.serialize("json",UserProfile.objects.filter(user=request.user)))
    apikey = tmpObj[0]['fields']['apikey']
    return  HttpResponse(f"Logged in.\n\nEmail: {request.user.email}\nUsername: {request.user.username}\nAPI Key: {apikey}")
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def ruofan(request):
    return HttpResponse("Ruofan's page...")
