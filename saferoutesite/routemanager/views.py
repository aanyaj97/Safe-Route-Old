from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from routemanager.models import Address, Route

def index(request):
	route = RequestContext(request)
	route_dict = {'route': 'This is how I will display a route.'}
	return render_to_response('routemanager/index.html', route_dict)