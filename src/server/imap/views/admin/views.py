# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

from imap.database import queries
import forms


def main_page(request):
    return render_to_response("admin/main.html")

def show_immobiles(request):
    objects = queries.get_all_immobiles_objects()
    return render_to_response("admin/show_immobiles.html", {'immobiles' : objects})

def del_immobile(request, id):
    _ = queries.delete_immobile_object(id)
    objects = queries.get_all_immobiles_objects()
    #return render_to_response("admin/show_immobiles.html", {'immobiles' : objects, 'message' : u"Объект #%s удален" % id})
    return HttpResponseRedirect('/admin/immobiles/')
    #return redirect("/admin/immobiles/", {'message' : 'Успешно удалено'})

def add_immobile(request):
    if request.method == 'POST':
        form = forms.ImmobileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            queries.add_immobile_object(data)
            return HttpResponseRedirect('/admin/immobiles/')
    else:
        form = forms.ImmobileForm()
    return render_to_response("admin/edit_immobile.html", {'form' : form, 'creating' : True})

def edit_immobile(request, id):
    if request.method == 'POST':
        form = forms.ImmobileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            queries.update_immobile_object(id, data)
            return HttpResponseRedirect('/admin/immobiles/')
    else:
        object = queries.get_immobile_object(id)
        form = forms.ImmobileForm(initial = object)
    return render_to_response("admin/edit_immobile.html", {'form' : form, 'creating' : False})



