# -*- coding: utf-8 -*-
from django import forms

class ImmobileForm(forms.Form):
    #return {'id' : id, 'name' : name, 'phone' : phone, 'latitude' : latitude, 'longitude' : longitude}
    #id = forms.()
    name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)