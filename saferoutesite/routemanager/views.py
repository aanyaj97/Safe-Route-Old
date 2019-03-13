import csv
import os

from django.shortcuts import render
from django import forms
from dijkstra_path1 import go


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
    date_of_travel = forms.DateField(
    	label= "Date of Travel",
    	help_text= "e.g. 10/10/2010 14:30",
    	required=False)
    time_of_travel = forms.TimeField(
    	label= "Date of Travel",
    	help_text= "e.g. 14:30",
    	required=False)


def plot_route(request):
    '''
    '''
    route_info = {}
    route = []
    if request.method == 'GET':
        address_form = AddressEntry(request.GET)
        route_info['response'] = address_form
        if address_form.is_valid():

            route = go(address_form.start_address, address_form.end_address,\
                       address_form.date_of_travel)
    route_info['route'] = route
    route_info['address_form'] = address_form

    return render(request, 'routemanager/index.html', route_info)