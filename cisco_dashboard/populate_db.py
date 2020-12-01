import meraki
import django, os, random

import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cisco_dashboard.settings')
django.setup()

from main.models import Organisation, Network, Device


#API_KEY = os.environ['X_Cisco_Meraki_API_Key']
#meraki.DEFAULT_BASE_URL = os.environ['base_Url']
API_KEY = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"

dash = meraki.DashboardAPI(API_KEY)

def updateAll(apikey):
    #dash = meraki.DashboardAPI(apikey)
    #updateOrganizations(dash,apikey)

    allOrgs = dash.organizations.getOrganizations()
    print(len(allOrgs))
    for i in range(18,20):
        org = allOrgs[i]
        updateNetwork(dash,org['id'])
       #for net in dash.organizations.getOrganizationNetworks(org['id']):
        #    updateDevices(dash,net['id'])

def updateOrganizations(dash,apikey):
    GETorgs = dash.organizations.getOrganizations() #Get all organizations

    for org in GETorgs:

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
        except:
            newOrg = Organisation.objects.create(
                orgID   = org['id'],
                orgName = org['name'],
                orgURL  = org['url'],
                apikey = apikey
                #orgAPIOverview = APIOverview
            )
            newOrg.save()

t = 0
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

    time.sleep(5)

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


updateAll(API_KEY)