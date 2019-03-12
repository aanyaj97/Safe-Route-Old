import csv
import os

from django.shortcuts import render
from django import forms


def load_valid_data(csv):
    '''
    '''
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'valid_data', csv)
    with open(csv_path) as data:
        return [line for line in data]

CHICAGO_ZIPS = load_valid_data('zip_codes.csv')

class AddressEntry(forms.Form):
    '''
    '''
    start_address = forms.CharField(
        label= "Start Address",
        help_text= "e.g. 1234 N Main St.",
        required= True)
    start_zip = forms.CharField(
        label= "Start Zipcode",
        help_text= "e.g. 60637",
        required= True)
    end_address = forms.CharField(
        label= "End Address",
        help_text= "e.g. 5000 N Main St.",
        required= True)
    end_zip = forms.CharField(
        label= "End Zipcode",
        help_text= "e.g. 60618",
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
            route = [[41.7952, -87.5964],[41.7917, -87.5964]]
    route_info['route'] = route
    route_info['address_form'] = address_form

    return render(request, 'routemanager/index.html', route_info)