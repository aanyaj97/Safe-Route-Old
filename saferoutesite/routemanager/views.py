import csv
import os

from django.shortcuts import render
from django import forms


class AddressEntry(forms.Form):
    '''
    '''
    start_address = forms.CharField(
        label= "Start Address",
        help_text= "e.g. 1234 N Main St.",
        required= True)
    end_address = forms.CharField(
        label= "End Address",
        help_text= "e.g. 5000 N Main St.",
        required= True)
    date_of_travel = forms.DateTimeField(
    	label= "Date of Travel",
    	help_text= "e.g. 10/10/2010 14:30",
    	required=True)
    temperature_at_travel = forms.IntegerField(
    	label= "Temperature in Farenheit at Time of Travel",
    	help_text= "e.g. 37",
    	required=True)


def plot_route(request):
    '''
    '''
    route_info = {}
    route = []
    if request.method == 'GET':
        address_form = AddressEntry(request.GET)
        route_info['response'] = address_form
        if address_form.is_valid():
            route = [[41.7952, -87.5964],[41.7917, -87.5964],[41.9405, -87.6390]]
    route_info['route'] = route
    route_info['address_form'] = address_form

    return render(request, 'routemanager/index.html', route_info)