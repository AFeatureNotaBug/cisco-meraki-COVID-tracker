"""
 * Views file
 * Contains all views used in the Cisco Dashboard web app
"""
import json
import math
import subprocess
import time
from datetime import datetime
import meraki

from django.shortcuts import render
from django.shortcuts import redirect
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.urls import reverse
import requests

from main.forms import UserForm
from main.forms import UserProfileForm

from main.models import Organisation
from main.models import Network
from main.models import Device
from main.models import UserProfile
from main.models import Snapshot
from main.models import AccessAlert


def index(request):
    """Index page view"""
    context_dict = {
        'users':len(UserProfile.objects.all()),
        'networks':len(Network.objects.all()),
        'orgs':len(Organisation.objects.all()),
        'devices':len(Device.objects.all())
    }

    response = render(
        request,
        'main/index.html',
        context = context_dict
    )

    return response


@login_required
def overview(request):
    """Main content"""
    uob = UserProfile.objects.filter(user = request.user)
    apikey = json.loads(serializers.serialize("json", uob))[0]['fields']['apikey']

    if apikey in (None, 'demo', '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'):
        print('NO APIKEY (use default)')
        apikey = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

    else:
        update_all(apikey)

    context_dict = {
        'allOrgs':  Organisation.objects.filter(apikey = apikey),
        'coords': dict(),
        'networks':0,
        'devices':0,
        'aps':0,
        'cameras':0,
    }

    for org in Organisation.objects.filter(apikey=apikey):
        context_dict[org.org_id] = Network.objects.filter(org = org)

        for net in list(Network.objects.filter(org = org)):
            context_dict['devices'] += len(Device.objects.filter(net=net))
            for device in Device.objects.filter(net=net):
                if device.devModel == 'MV12N':
                    context_dict['cameras'] += 1
                elif device.devModel =='MR30H':
                    context_dict['aps'] +=1
            context_dict['networks'] += 1
            context_dict['coords'][net.net_id] = get_coords(net.scanningAPIURL)

    context_dict['coords'] = json.dumps(context_dict['coords'])

    return render(request, 'main/overviewPage.html', context = context_dict)


@login_required
def alerts_page(request):
    """Alerts page"""
    user = UserProfile.objects.get(user=request.user)

    try:
        org = Organisation.objects.get(apikey=user.apikey)

    except Organisation.DoesNotExist:
        #print('\n\n\norg doesnt exist\n\n\n')
        return render(request, 'main/alerts.html', context = {"snapshots":[]})

    user_snapshots = Snapshot.objects.filter(org =org)

    context_dict = {
        "snapshots": list(user_snapshots)
    }

    return render(request, 'main/alerts.html', context = context_dict)


@login_required
def usedemokey(request):
    """Updates use API key to demo key"""

    user_to_update = UserProfile.objects.filter(user=request.user)

    user_to_update.update(
        apikey = 'demo'
    )

    return redirect('/profile')


@login_required
def editapikey(request):
    """Allows user to edit their API key"""

    user_to_update = UserProfile.objects.filter(user=request.user)
    error = False
    try:
        meraki.DashboardAPI(request.POST['apikey']).organizations.getOrganizations()
    except meraki.exceptions.APIError:
        error=True

    user_to_update.update(
        apikey = request.POST['apikey']
    )

    tmp_obj = json.loads(
        serializers.serialize(
            "json",
            UserProfile.objects.filter(user = request.user)
        )
    )

    retapikey = None
    scanning_api_url = None

    try:
        apikey = tmp_obj[0]['fields']['apikey']
        retapikey = (len(apikey) - 4) * '*' + apikey[-4:]
        scanning_api_url = tmp_obj[0]['fields']['apikey']

    except IndexError:
        apikey = 'Not found'

    context_dict = {
        'email': request.user.email,
        'username': request.user.username,
        'apikey': retapikey,
        'scanningAPIURL': scanning_api_url,
        'error':error
    }

    return render(request, 'main/profile.html',context=context_dict)


def register(request):
    """
    View for register page
     * Allows users to register for an account
    """

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile_form = profile_form.save(commit = False)
            profile_form.user = user
            profile_form.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }

    return render(request, 'main/register.html', context = context_dict)


def user_login(request):
    """
    User login view
     * Allows users with existing accounts to log in
    """

    render_url = "main/login.html"
    context_dict = dict()
    redirect_status = False

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)


        if user:
            if user.is_active:
                login(request, user)
                redirect_status = True

            else:
                context_dict = {
                    'error': {
                        'title': 'Account disabled',
                        'message': 'You login account has been disabled, it is no longer active.'
                    }
                }

                render_url = "main/error.html"

        else:
            context_dict = {
                "error": {
                    'title': 'Invalid login credentials',
                    'message': "The username or password you \
                        provided us was invalid. Please try again.",

                    "bold": f"Username: {username}"
                }
            }

            render_url = "main/error.html"

    if redirect_status:
        return redirect('/profile')

    return render(request, render_url, context = context_dict)


@login_required
def profile(request):
    """
    Profile view
     * Allows logged-in users to view their profile information
    """

    tmp_obj = json.loads(
        serializers.serialize(
            "json",
            UserProfile.objects.filter(user = request.user)
        )
    )

    retapikey = None
    scanning_api_url = None

    try:
        apikey = tmp_obj[0]['fields']['apikey']
        retapikey = (len(apikey) - 4) * '*' + apikey[-4:]
        scanning_api_url = tmp_obj[0]['fields']['apikey']

    except IndexError:
        apikey = 'Not found'

    context_dict = {
        'email': request.user.email,
        'username': request.user.username,
        'apikey': retapikey,
        'scanningAPIURL': scanning_api_url
    }

    return render(request, 'main/profile.html', context = context_dict)


@login_required
def user_logout(request):
    """
    Logout view
     * Allows logged-in users to log out
     * Redirects users to index page
    """

    logout(request)

    return redirect(reverse('index'))


def update_orgs(apikey):
    """Calls function to update organisations"""
    dash = meraki.DashboardAPI(apikey)
    update_organisations(dash, apikey)


def update_all_networks(apikey):
    """
    Calls function to update networks
    """

    dash = meraki.DashboardAPI(apikey)
    update_organisations(dash, apikey)

    try:
        orgs = dash.organizations.getOrganizations()
    except meraki.exceptions.APIError:
        print('401 api key invalid')
        return

    for org in orgs:
        update_network(dash,org['id'])


def update_all(apikey):
    """
    Calls functions to update both organisations and networks
    """

    dash = meraki.DashboardAPI(apikey)
    update_organisations(dash,apikey)
    try:
        for org in dash.organizations.getOrganizations():
            update_network(dash,org['id'])
            for net in dash.organizations.getOrganizationNetworks(org['id']):
                update_devices(dash,net['id'])
    except meraki.exceptions.APIError:
        print('401 api key invalid')
        return

def update_organisations(dash, apikey):
    """
    Updates organisations in database
    """

    try:
        get_orgs = dash.organizations.getOrganizations() #Get all organizations
    except meraki.exceptions.APIError:
        print('401 api key invalid')
        return
    for org in get_orgs:

        try:
            Organisation.objects.get(org_id=org['id'])
            org_to_update = Organisation.objects.filter(org_id=org['id'])

            org_to_update.update(
                org_id   = org['id'],
                org_name = org['name'],
                org_url  = org['url'],
                apikey = apikey
                #orgAPIOverview = APIOverview
            )

        except Organisation.DoesNotExist:
            new_org = Organisation.objects.create(
                org_id   = org['id'],
                org_name = org['name'],
                org_url  = org['url'],
                apikey = apikey
                #orgAPIOverview = APIOverview
            )
            new_org.save()


#updates all networks for an organization ID
def update_network(dash,org_id):
    """Updates networks in database"""
    get_nets = dash.organizations.getOrganizationNetworks(org_id)
    new_org = Organisation.objects.get(org_id=org_id)

    for net in get_nets:
        try:
            Network.objects.get(net_id = net['id'])
            net_to_update = Network.objects.filter(net_id = net['id'])

            net_to_update.update(
                org     = new_org,
                net_id   = net['id'],
                net_name = net['name']
            )

        except Network.DoesNotExist:
            new_net = Network.objects.create(
                org     = new_org,
                net_id   = net['id'],
                net_name = net['name']
            )

            new_net.save()


#updates all devices for a network ID
def update_devices(dash,net_id):
    """
    Updates devices in database
    """

    try:
        get_devices = dash.networks.getNetworkDevices(net_id)
        new_net = Network.objects.get(net_id = net_id)

    except meraki.exceptions.APIError:
        print('401 api key invalid')
        return

    for device in get_devices:
        dev = None

        try:
            dev = Device.objects.get(devSerial = device['serial'])

            dev.devAddr   = device['address']
            dev.devSerial = device['serial']
            dev.devMac    = device['mac']
            dev.devModel  = device['model']

            dev.devLat    = device['lat']
            dev.devLong   = device['lng']

        except Device.DoesNotExist:
            dev = Device.objects.create(
                net = new_net,

                devAddr   = device['address'],

                devSerial = device['serial'],
                devMac    = device['mac'],
                devModel  = device['model'],
                #devLanIP  = device['lanIp'],

                devLat    = device['lat'],
                devLong   = device['lng']
            )
            dev.save()

        try:
            device_model = dev.devModel

            if device_model == "MV12N": #See if device is a camera
                subprocess.Popen(
                    ["python", "camera.py", device['serial']],    #Launch cron.py with device model
                    stdin  = None,
                    stdout = None,
                    stderr = None,
                    close_fds = True
                )

        except Device.DoesNotExist:
            print("Error initialising camera")


def edit_scanning_api_url(request):
    """Allows user to edit their API key"""
    if request.POST['scanningAPIURL'] in ("",None):
        return ["Please set your scanning API URL in your profile"]
    #creation of map comes here + business logic

    body = {"key":"randominsert!!222_"}
    resp = requests.post(request.POST['scanningAPIURL'], body, {"Content-Type":"application/json"})


    try:
        resp.json()
    except json.decoder.JSONDecodeError:
        return redirect('/overview')
    network_to_update = Network.objects.filter(net_id=request.POST['net_id'])
    network_to_update.update(
        scanningAPIURL = request.POST['scanningAPIURL']
    )

    return redirect('/overview')


def get_coords(scanning_api_url):
    """ gets coordinates of scanning api url"""
    if scanning_api_url in ("",None):
        return ["Please set your scanning API URL in your profile"]
    #creation of map comes here + business logic

    body = {"key":"randominsert!!222_"}
    resp = requests.post(scanning_api_url, body, {"Content-Type":"application/json"})

    try:
        resp_json = resp.json()

    except json.decoder.JSONDecodeError:
        return []

    for outer in resp_json['body']['data']['observations']:
        dist_list = []

        for inn in resp_json['body']['data']['observations']:

            if outer != inn:
                outer_long = outer['location']['lng']
                outer_lat  = outer['location']['lat']

                inner_long = inn['location']['lng']
                inner_lat  = inn['location']['lat']

                hav = haversine(outer_long, outer_lat, inner_long, inner_lat)

                if hav < 2 and hav == 0:
                    text = "<span style='color:red'>" + "%.2f" % hav

                else:
                    text = "<span style='color:green'>" + "%.2f" % hav

                    new_access_alert = AccessAlert.objects.create(  #Add new AP alert
                        org = Organisation.objects.filter(
                            apikey = "4f9d726866f2cb8da55221caf1f46ba34293449c"
                            )[0],
                        dev_type_1 = outer['manufacturer'],
                        dev_type_2 = inn['manufacturer'],
                        time       = str(datetime.fromtimestamp(time.time()).isoformat())
                    )
                    new_access_alert.save()

                text+= ' - ' + inn['clientMac'] + '</span>'
                dist_list.append(text)

        outer['distances'] = dist_list

    return resp_json['body']['data']['observations']


def haversine(lat1, lon1, lat2, lon2):
    """ An implementation of the haversine formula to
    caluclate distance between 2 points (long,lat) on earth)"""
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    arcsin = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) ** 2

    result = 2 * math.asin(math.sqrt(arcsin))
    radius = 6371.1370 # Radius of earth km

    return result * radius * 1000
