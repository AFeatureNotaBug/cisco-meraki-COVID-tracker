from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

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
    return HttpResponse("Jake's page...")

def johnathan(request):
    return HttpResponse("Johnathan's page...")

def ruofan(request):
    return HttpResponse("Ruofan's page...")