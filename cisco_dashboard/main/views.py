from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext


import matplotlib.pyplot as plt
from random import randint as r
import io, urllib, base64

from django.shortcuts import render, redirect
from .forms import RegisterForm

import meraki
from main.models import Organisation
from main.models import Network

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
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
	    form = RegisterForm()

    return render(response, "main/register.html", {"form":form})


def ruofan(request):
    return HttpResponse("Ruofan's page...")
