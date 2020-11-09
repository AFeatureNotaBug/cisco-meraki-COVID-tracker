import meraki
import django, os, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cisco_dashboard.settings')
django.setup()

from main.models import Organisation, Network, Device


#API_KEY = os.environ['X_Cisco_Meraki_API_Key']
#meraki.DEFAULT_BASE_URL = os.environ['base_Url']
API_KEY = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"

dash = meraki.DashboardAPI(API_KEY)
GETorgs = dash.organizations.getOrganizations() #Get all organizations

for org in GETorgs:

    #past 24 hours
    #APIOverview = dash.organizations.getOrganizationApiRequestsOverview(org['id'],timespan=60*60*24)

    newOrg = Organisation.objects.create(
        orgID   = org['id'],
        orgName = org['name'],
        orgURL  = org['url'],
        #orgAPIOverview = APIOverview
    )
    newOrg.save()
    
    GETnets = dash.organizations.getOrganizationNetworks(org['id'])
    
    for net in GETnets:
        newNet = Network.objects.create(
            org     = newOrg,
            netID   = net['id'],
            netName = net['name']
        )
        newNet.save()
        
        GETdevs = dash.networks.getNetworkDevices(net['id'])
        
        for device in GETdevs:
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

