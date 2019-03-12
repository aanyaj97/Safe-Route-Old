from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from routemanager.models import Address, Route

def index(request):
    route = RequestContext(request)
    route_dict = {'route': 'This is how I will display a route.', 'start':[[41.7952, -87.5964],\
    [41.7917, -87.5964], [41.7913, -87.5866]]} 

    return render_to_response('routemanager/index.html', route_dict)