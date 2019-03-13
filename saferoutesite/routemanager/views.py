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
         #   if address_form.start_zip not in CHICAGO_ZIPS:
         #       route_info['start_zip']= 'Please enter in a valid starting zipcode.'
         #   if address_form.start_zip not in CHICAGO_ZIPS:
         #       route_info['end_zip']= 'Please enter in a valid ending zipcode.'
             #else:
            route = [[41.7860077, -87.5915829],
 [41.786084, -87.5915886],
 [41.7860656, -87.5930936],
 [41.7860584, -87.5939084],
 [41.7860563, -87.5947086],
 [41.7860209, -87.5962285],
 [41.7860071, -87.5963328],
 [41.786395, -87.5963427],
 [41.786507, -87.5963454],
 [41.7865942, -87.5963475],
 [41.7871639, -87.5963608],
 [41.7872257, -87.5963623],
 [41.7873622, -87.5963655],
 [41.7877215, -87.5963739],
 [41.7878006, -87.5963758],
 [41.7877991, -87.5964793],
 [41.7877799, -87.5979926],
 [41.7877789, -87.5980809],
 [41.7877738, -87.5985516],
 [41.7877653, -87.5996084],
 [41.7877569, -87.6006483],
 [41.7877532, -87.601111],
 [41.7877523, -87.6012275],
 [41.7877508, -87.601339],
 [41.7877214, -87.6035258],
 [41.7877191, -87.6036965],
 [41.7877048, -87.6047606],
 [41.7877027, -87.6049106],
 [41.7877871, -87.6049124],
 [41.7895302, -87.6049492],
 [41.7895401, -87.6036972],
 [41.7895513, -87.602465],
 [41.7895926, -87.6024668],
 [41.7902233, -87.6024821],
 [41.7902469, -87.6024462]]
    route_info['route'] = route
    route_info['address_form'] = address_form

    return render(request, 'routemanager/index.html', route_info)