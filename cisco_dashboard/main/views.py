"""
 * Views file
 * Contains all views used in the Cisco Dashboard web app
"""

import json
import math
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


def index(request):
    """Index page view"""
    context_dict = {
        'example_text': 'THIS IS EXAMPLE TEXT',
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
        update_orgs(apikey)
        update_all_networks(apikey)

    context_dict = {
        'allOrgs':  Organisation.objects.filter(apikey = apikey),
        'coords': dict()
    }

    for org in Organisation.objects.filter(apikey=apikey):
        context_dict[org.org_id] = Network.objects.filter(org = org)

        for net in list(Network.objects.filter(org = org)):
            context_dict['coords'][net.net_id] = get_coords(request, net.scanningAPIURL)

    context_dict['coords'] = json.dumps(context_dict['coords'])

    return render(request, 'main/overviewPage.html', context = context_dict)


@login_required
def alerts_page(request):
    """Alerts page"""
    user_snapshots = Snapshot.objects.filter(user = request.user)
    
    context_dict = {
        "snapshots": [s for s in user_snapshots]
        #'response': response['url']
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

    user_to_update.update(
        apikey = request.POST['apikey']
    )

    return redirect('/profile')


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

    for org in dash.organizations.getOrganizations():
        update_network(dash,org['id'])


def update_all(apikey):
    """
    Calls functions to update both organisations and networks
    """

    dash = meraki.DashboardAPI(apikey)
    update_organisations(dash,apikey)

    for org in dash.organizations.getOrganizations():
        update_network(dash,org['id'])
        #for net in dash.organizations.getOrganizationNetworks(org['id']):
        #update_devices(dash,net['id'])


def update_organisations(dash, apikey):
    """
    Updates organisations in database
    """

    get_orgs = dash.organizations.getOrganizations() #Get all organizations

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

    get_devices = dash.networks.getNetworkDevices(net_id)
    new_net= Network.objects.get(net_id=net_id)

    for device in get_devices:
        try:
            Device.objects.get(devSerial = device['serial'])

            dev_to_update = Device.objects.filter(devSerial = device['serial'])
            dev_to_update.update(
                net = new_net,

                devAddr   = device['address'],
                devSerial = device['serial'],
                devMac    = device['mac'],
                devModel  = device['model'],
                #devLanIP  = device['lanIp'],

                devLat    = device['lat'],
                devLong   = device['lng']
            )

        except Device.DoesNotExist:
            new_device = Device.objects.create(
                net = new_net,

                devAddr   = device['address'],

                devSerial = device['serial'],
                devMac    = device['mac'],
                devModel  = device['model'],
                #devLanIP  = device['lanIp'],

                devLat    = device['lat'],
                devLong   = device['lng']
                )
            new_device.save()


def edit_scanning_api_url(request):
    """Allows user to edit their API key"""
    network_to_update = Network.objects.filter(net_id=request.POST['net_id'])
    network_to_update.update(
        scanningAPIURL = request.POST['scanningAPIURL']
    )

    return redirect('/overview')


def get_coords(request, scanning_api_url):
    """ gets coordinates of scanning api url"""
    if scanning_api_url in ("",None):
        return ["Please set your scanning API URL in your profile"]
    #creation of map comes here + business logic

    body = {"key":"randominsert!!222_"}
    resp = requests.post(scanning_api_url, body, {"Content-Type":"application/json"})
    
    print("\n\n\n", resp, "\n\n\n")
    print(resp.json(), "\n\n\n")
    
    resp_json = resp.json()
    for outter in range(len(resp_json['body']['data']['observations'])):
        dist_list = []
        for inn in resp_json['body']['data']['observations']:
            long = resp_json['body']['data']['observations'][outter]['location']['lng']
            lat = resp_json['body']['data']['observations'][outter]['location']['lat']
            hav = haversine(long,lat,inn['location']['lng'],inn['location']['lat'])
            if hav < 2:
                text = "<span style='color:red'>" + "%.2f" % hav

                #Create snapshot if more than one person in camera zone (entire frame)
                tmp_obj = json.loads(
                    serializers.serialize(
                        "json",
                        UserProfile.objects.filter(user = request.user)
                    )
                )

                apikey = tmp_obj[0]['fields']['apikey'] #Get apikey
                dash = meraki.DashboardAPI(apikey)

                serial = "Q2EV-TWQP-G8VX"   #Temp hardcoded serial number for ben home camera

                #analytics_response = dash.camera.getDeviceCameraAnalyticsOverview(serial)
                #if analytics_response['entrances'] > 1: #More than one person in zone

                url_response = dash.camera.generateDeviceCameraSnapshot(serial) #Pic
                all_users = UserProfile.objects.filter(user = request.user)

                for user_profile in all_users:
                    new_snapshot = Snapshot.objects.create(
                        user = user_profile.user,
                        url = url_response['url'],
                        time = 1
                    )
                    new_snapshot.save()

            else:
                text = "<span style='color:green'>" + "%.2f" % hav
            text+= ' - ' + inn['clientMac'] + '</span>'
            dist_list.append(text)

        resp_json['body']['data']['observations'][outter]['distances'] = dist_list
    
    print("\n\n\n\n")
    print(resp_json)
    print("\n\n\n\n")
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
