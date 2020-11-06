from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext
from django.core import serializers

import matplotlib.pyplot as plt
from random import randint as r
import io, urllib, base64
import json
from django.core.serializers.json import DjangoJSONEncoder


import meraki
from main.models import Organisation, Network, Device

# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the main index.")

    response = render(request, 'main/index.html', context = {'example_text' : 'THIS IS EXAMPLE TEXT',})
    return response


def ben(request):
    return render(request, "main/benPage.html") 


def fraser(request):
    #print(serializers.serialize('json', [Organisation.objects.all(),]))
    tmpObj = json.loads(serializers.serialize("json",Organisation.objects.all()))
    return render(request, 'main/fraser.html', context = {'organisations':{'data':json.dumps(tmpObj, indent=4, sort_keys=True),'meta':{'number':len(Organisation.objects.all())}}})
    
    
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


def showOrg(request, org_slug):
    organisation = Organisation.objects.get(slug = org_slug)
    networks = Network.objects.filter(org = organisation)
    
    context_dict = {
        'org': organisation,
        'net': networks
    }
    
    return render(request, "main/orgPage.html", context = context_dict)


def showNet(request, org_slug, net_slug):
    network = Network.objects.get(slug = net_slug)
    devices = Device.objects.filter(net = network)
    
    context_dict = {
        'net': network,
        'devices': devices
    }
    
    return render(request, "main/netPage.html", context = context_dict)
    

def johnathan(request):
    return HttpResponse("Johnathan's page...")


def ruofan(request):
    return HttpResponse("Ruofan's page...")
