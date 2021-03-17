from main.models import Organisation
from main.models import Network
from main.models import Device
from main.models import Snapshot
from main.models import UserProfile
from django.core import serializers
import requests
import json
import math
import meraki
import datetime
import time

def get_coords(scanning_api_url,apikey,serial):
    """ gets coordinates of scanning api url"""
    if scanning_api_url in ("",None):
        return ["Please set your scanning API URL in your profile"]
    #creation of map comes here + business logic

    body = {"key":"randominsert!!222_"}
    resp = requests.post(scanning_api_url, body, {"Content-Type":"application/json"})
    found = False

    resp_json = resp.json()
    for outter in range(len(resp_json['body']['data']['observations'])):
        dist_list = []
        for inn in resp_json['body']['data']['observations']:
            long = resp_json['body']['data']['observations'][outter]['location']['lng']
            lat = resp_json['body']['data']['observations'][outter]['location']['lat']
            hav = haversine(long,lat,inn['location']['lng'],inn['location']['lat'])
            if hav < 2:
                text = "<span style='color:red'>" + "%.2f" % hav
                found = True
            else:
                text = "<span style='color:green'>" + "%.2f" % hav
            text+= ' - ' + inn['clientMac'] + '</span>'
            dist_list.append(text)

        resp_json['body']['data']['observations'][outter]['distances'] = dist_list

    #if found:
        #Create snapshot if more than one person in camera zone (entire frame)
        #dash = meraki.DashboardAPI(apikey)

        #analytics_response = dash.camera.getDeviceCameraAnalyticsOverview(serial)

        #if analytics_response['entrances'] > 1: #More than one person in zone
        #url_response = dash.camera.generateDeviceCameraSnapshot(serial) #Pic
        #current_time = datetime.datetime.now()

        #all_users = UserProfile.objects.filter(apikey = apikey)

        #for user_profile in all_users:
            #new_snapshot = Snapshot.objects.create(
                #user = user_profile.user,
                #url = url_response['url'],
                #time = current_time.strftime("%c")
            #)
            #new_snapshot.save()

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


while True:
    for user in list((UserProfile.objects.all())):
        for org in list((Organisation.objects.filter(apikey=user.apikey))):
            print(org.apikey)
            for net in (Network.objects.filter(org=org)):
                
                if(net.scanningAPIURL != None):
                    #get_coords(network.scanningAPIURL)
                    for device in list((Device.objects.filter(net=net))):
                        if (device.devModel == 'MV12N'):
                            get_coords(net.scanningAPIURL,user.apikey,device.devSerial) 
    time.sleep(60)