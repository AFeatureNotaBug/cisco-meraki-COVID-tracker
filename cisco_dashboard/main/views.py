from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
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
from django.core import serializers

import matplotlib.pyplot as plt
from random import randint as r
import io, urllib, base64
import json
#from django.core.serializers.json import DjangoJSONEncoder


import meraki
from main.models import Organisation, Network, Device


def index(request):
    #return HttpResponse("Hello, world. You're at the main index.")

    response = render(request, 'main/index.html', context = {'example_text' : 'THIS IS EXAMPLE TEXT',})
    return response
    

def overview(request):
    updateAll('6bec40cf957de430a6f1f2baa056b99a4fac9ea0')
    context_dict = {
        'allOrgs':  Organisation.objects.all(),
    }
    
    for org in Organisation.objects.all():
        context_dict[org.orgID] = Network.objects.filter(org = org)
    
    return render(request, 'main/overviewPage.html', context = context_dict)


# View for register page
def register(request):
    """ if request.user:
        return redirect('/profile') """
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
    """ if request.user:
        return redirect('/profile') """
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
    try:
        apikey = tmpObj[0]['fields']['apikey']
    except:
        apikey = 'Not found'
    return render(request, 'main/profile.html', context={'email':request.user.email,'username':request.user.username,'apikey':apikey})
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def updateAll(apikey):
    dash = meraki.DashboardAPI(apikey)
    updateOrganizations(dash)
    for org in dash.organizations.getOrganizations():
        updateNetwork(dash,org['id'])
        #for net in dash.organizations.getOrganizationNetworks(org['id']):
        #    updateDevices(dash,net['id'])

def updateOrganizations(dash):
    GETorgs = dash.organizations.getOrganizations() #Get all organizations

    for org in GETorgs:

        try:
            Organisation.objects.get(orgID=org['id'])
            org_to_update = Organisation.objects.filter(orgID=org['id'])
            org_to_update.update(
                orgID   = org['id'],
                orgName = org['name'],
                orgURL  = org['url'],
                #orgAPIOverview = APIOverview
            )
        except:
            newOrg = Organisation.objects.create(
                orgID   = org['id'],
                orgName = org['name'],
                orgURL  = org['url'],
                #orgAPIOverview = APIOverview
            )
            newOrg.save()
    


#updates all networks for an organization ID
def updateNetwork(dash,orgID):
    GETnets = dash.organizations.getOrganizationNetworks(orgID)
    newOrg = Organisation.objects.get(orgID=orgID)
    for net in GETnets:
        try:
            Network.objects.get(netID = net['id'])
            net_to_update = Network.objects.filter(netID = net['id'])
            net_to_update.update(
                    org     = newOrg,
                    netID   = net['id'],
                    netName = net['name']
            )
        except:
            newNet = Network.objects.create(
                    org     = newOrg,
                    netID   = net['id'],
                    netName = net['name']
            )
            newNet.save()

#updates all devices for a network ID
def updateDevices(dash,netID):
    GETdevs = dash.networks.getNetworkDevices(netID)
    newNet= Network.objects.get(netID=netID)
            
    for device in GETdevs:
        try:
            Device.objects.get(devSerial = device['serial'])
            dev_to_update = Device.objects.filter(devSerial = device['serial'])
            dev_to_update.update(
                net = newNet, 
                        
                devAddr   = device['address'],
                        
                devSerial = device['serial'],
                devMac    = device['mac'],
                devModel  = device['model'],
                        #devLanIP  = device['lanIp'],
                        
                devLat    = device['lat'],
                devLong   = device['lng']
                )
        except:
            newDevice = Device.objects.create(
                net = newNet,

                devAddr   = device['address'],
                        
                devSerial = device['serial'],
                devMac    = device['mac'],
                devModel  = device['model'],
                        #devLanIP  = device['lanIp'],
                        
                devLat    = device['lat'],
                devLong   = device['lng']
                )
            newDevice.save()
