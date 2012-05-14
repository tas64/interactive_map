# -*- coding: utf-8 -*-
from django import forms

class ImmobileForm(forms.Form):
    #return {'id' : id, 'name' : name, 'phone' : phone, 'latitude' : latitude, 'longitude' : longitude}
    #id = forms.()
    name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)

class MovableForm(forms.Form):
    #return {'id' : id, 'name' : name, 'type' : type}
    name = forms.CharField(required=True)

class MovableTypeForm(forms.Form):
    #return {'id' : id, 'name' : name}
    name = forms.CharField(required=True)

class UploadFileForm(forms.Form):
    file = forms.FileField()