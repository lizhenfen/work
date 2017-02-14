from django.shortcuts import render_to_response
from  django.http import  HttpResponse
# Create your views here.

def home(request):
    return  HttpResponse("hellp")

def servers(request):
    return render_to_response('cmdb/servers.html')