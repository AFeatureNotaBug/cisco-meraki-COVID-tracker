"""
 * Views file
 * Contains all views used in the Cisco Dashboard web app
"""

import json
import meraki

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.urls import reverse
import folium, requests


from django.core import serializers

from main.forms import UserForm
from main.forms import UserProfileForm

from main.models import Organisation
from main.models import Network
from main.models import Device
from main.models import UserProfile


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
    apikey =json.loads(serializers.serialize("json",UserProfile.objects.filter(user=request.user)))[0]['fields']['apikey']
    print(apikey)
    if(apikey == None or  apikey== 'demo' or apikey == '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'):
        print('NO APIKEY (use default)')
        apikey = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

    else:
        update_orgs(apikey)
        update_all_networks(apikey)

    context_dict = {
        'allOrgs':  Organisation.objects.filter(apikey = apikey),
        'coords':{}
    }
    
    for org in Organisation.objects.filter(apikey=apikey):
        context_dict[org.orgID] = Network.objects.filter(org = org)
        for net in list(Network.objects.filter(org = org)):
            context_dict['coords'][net.netID] = get_coords(net.scanningAPIURL)
    
    context_dict['coords'] = json.dumps(context_dict['coords'])
    return render(request, 'main/overviewPage.html', context = context_dict)


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

    try:
        apikey = tmp_obj[0]['fields']['apikey']
        retapikey = (len(apikey) - 4) * '*' + apikey[-4:]
        #scanningAPIURL = tmp_obj[0]['fields']['scanningAPIURL']

    except IndexError:
        apikey = 'Not found'

    context_dict = {
        'email': request.user.email,
        'username': request.user.username,
        'apikey': retapikey,
        #'scanningAPIURL':scanningAPIURL
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
    """
    Calls function to update organisations
    """

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
            Organisation.objects.get(orgID=org['id'])
            org_to_update = Organisation.objects.filter(orgID=org['id'])

            org_to_update.update(
                orgID   = org['id'],
                orgName = org['name'],
                orgURL  = org['url'],
                apikey = apikey
                #orgAPIOverview = APIOverview
            )

        except Organisation.DoesNotExist:
            new_org = Organisation.objects.create(
                orgID   = org['id'],
                orgName = org['name'],
                orgURL  = org['url'],
                apikey = apikey
                #orgAPIOverview = APIOverview
            )
            new_org.save()



#updates all networks for an organization ID
def update_network(dash,orgID):
    """
    Updates networks in database
    """

    get_nets = dash.organizations.getOrganizationNetworks(orgID)
    new_org = Organisation.objects.get(orgID=orgID)

    for net in get_nets:
        try:
            Network.objects.get(netID = net['id'])
            net_to_update = Network.objects.filter(netID = net['id'])

            net_to_update.update(
                org     = new_org,
                netID   = net['id'],
                netName = net['name']
            )

        except Network.DoesNotExist:
            new_net = Network.objects.create(
                org     = new_org,
                netID   = net['id'],
                netName = net['name']
            )

            new_net.save()


#updates all devices for a network ID
def update_devices(dash,netID):
    """
    Updates devices in database
    """

    get_devices = dash.networks.getNetworkDevices(netID)
    new_net= Network.objects.get(netID=netID)

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
            newDevice = Device.objects.create(
                net = new_net,

                devAddr   = device['address'],

                devSerial = device['serial'],
                devMac    = device['mac'],
                devModel  = device['model'],
                #devLanIP  = device['lanIp'],

                devLat    = device['lat'],
                devLong   = device['lng']
                )
            newDevice.save()

def get_map(scanningAPIURL):  

    #scanningAPIURL =json.loads(serializers.serialize("json",UserProfile.objects.filter(user=request.user)))[0]['fields']['scanningAPIURL']
    if(scanningAPIURL == "" or scanningAPIURL == None):
        return {'my_map':"Please set your scanning API URL in your profile"}
    #creation of map comes here + business logic
    
    try:
        d = requests.post(scanningAPIURL,{"key":"randominsert!!222_"},{"Content-Type":"application/json"})
        print(d.json())
        respJson = d.json()
        print(respJson['body'])
        m = folium.Map(zoom_start=18, max_zoom=18)
        for x in respJson['body']['data']['observations']:
            print(x['location']['lat'],x['location']['lng'])
            test = folium.Html(x['clientMac'], script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.CircleMarker(location=[x['location']['lat'],x['location']['lng']], radius=2, popup=popup).add_to(m)
        
        m.fit_bounds(m.get_bounds())
        m=m._repr_html_() #updated
        
        return {'my_map': m}

        
    except:
        return {'my_map':"Error retrieving info from scanning API"}

def get_coords(scanningAPIURL):
    if(scanningAPIURL == "" or scanningAPIURL == None):
        return ["Please set your scanning API URL in your profile"]
    #creation of map comes here + business logic
    
    try:
        d = requests.post(scanningAPIURL,{"key":"randominsert!!222_"},{"Content-Type":"application/json"})
        respJson = d.json()
        return respJson['body']['data']['observations']
    except:
        return []

def editScanningAPIURL(request):
    """Allows user to edit their API key"""

    network_to_update = Network.objects.filter(netID=request.POST['netID'])
    network_to_update.update(
        scanningAPIURL = request.POST['scanningAPIURL']
    )

    return redirect('/overview')