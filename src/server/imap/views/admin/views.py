# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

from imap.database import queries
import forms


def main_page(request):
    return render_to_response("admin/main.html")

def show_immobiles(request):
    objects = queries.get_all_immobiles_objects()
    return render_to_response("admin/show_immobiles.html", {'objects' : objects})

def del_immobile(request, id):
    _ = queries.delete_immobile_object(id)
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


def show_movables(request):
    objects = queries.get_all_movables_objects_with_types()
    return render_to_response("admin/show_movables.html", {'objects' : objects})

def del_movable(request,id):
    _ = queries.delete_movable_object(id)
    return HttpResponseRedirect('/admin/movables/')

def add_movable(request):
    if request.method == 'POST':
        form = forms.MovableForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            queries.add_movable_object(request.POST['movable_type'], data)
            return HttpResponseRedirect('/admin/movables/')
    else:
        form = forms.MovableForm()
    types = queries.get_all_movable_types()
    return render_to_response("admin/edit_movable.html", {'form' : form,  'types' : types, 'movable_type_id' : 0, 'creating' : True})

def edit_movable(request, id):
    movable_type_id = 0
    if request.method == 'POST':
        form = forms.MovableForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            queries.update_movable_object(id, request.POST['movable_type'], data)
            return HttpResponseRedirect('/admin/movables/')
    else:
        object = queries.get_movable_object(id)
        movable_type_id = object['movable_type_id']
        form = forms.MovableForm(initial = object)
    types = queries.get_all_movable_types()
    return render_to_response("admin/edit_movable.html", {'form' : form,  'types' : types, 'movable_type_id' : movable_type_id,  'creating' : False})


def show_movable_types(request):
    objects = queries.get_all_movable_types()
    return render_to_response("admin/show_movable_types.html", {'objects' : objects})

def del_movable_type(request,id):
    _ = queries.delete_movable_type(id)
    return HttpResponseRedirect('/admin/movable_types/')

def add_movable_type(request):
    if request.method == 'POST':
        form = forms.MovableTypeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['movable_type_id'] = request.POST['movable_type_id']
            queries.add_movable_type(data)
            return HttpResponseRedirect('/admin/movable_types/')
    else:
        form = forms.MovableTypeForm()
    return render_to_response("admin/edit_movable_type.html", {'form' : form, 'creating' : True})

def edit_movable_type(request, id):
    if request.method == 'POST':
        form = forms.MovableTypeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            queries.update_movable_type(id, data)
            return HttpResponseRedirect('/admin/movable_types')
    else:
        object = queries.get_movable_type(id)
        form = forms.MovableTypeForm(initial = object)
    return render_to_response("admin/edit_movable_type.html", {'form' : form, 'creating' : False})



