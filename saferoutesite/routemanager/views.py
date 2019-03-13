import csv
import os
import datetime

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
    hour_of_travel = forms.TimeField(
    	label= "Date of Travel",
    	help_text= "e.g. 14",
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
            start = address_form.cleaned_data['start_address']
            end = address_form.cleaned_data['end_address']
            current_DT = datetime.datetime.now()
            date_string = current_DT.strftime('%Y-%m-%d')
            time_string = current_DT.hour
            route = go(start, end, date_string, time_string)
    route_info['route'] = route
    route_info['address_form'] = address_form

    return render(request, 'routemanager/index.html', route_info)