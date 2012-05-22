# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from psycopg2._psycopg import IntegrityError

from imap.database import queries
import forms

import re

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
    return render_to_response("admin/edit_movable.html", {'id': id, 'form' : form,  'types' : types, 'movable_type_id' : movable_type_id,  'creating' : False})


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


def handle_file(content):
    content.replace('\r','') #will handle both: windows and linux-formatted files
    counter = 0
    for line in content.split('\n'):
        if not line.startswith('$'):
            continue
        line = re.sub(r"\s", "", line)
        id, time, latitude, p, longitude, j = line[1:].split(',')

        if (p != 'S' and p != 'N') or (j != 'E' and j != 'W'):
            continue

        h,m,s = time[0:2], time[2:4], time[4:]
        latitude_degree, latitude_minute = int(latitude[0:2]), float(latitude[2:])
        longitude_degree, longitude_minute = int(longitude[0:2]), float(longitude[2:])

        real_latitude = float(latitude_degree) + float(latitude_minute/60)
        real_longitude = float(longitude_degree) + float(longitude_minute/60)

        if p == 'S':
            real_latitude *= -1
        if j == 'E':
            real_longitude *= -1

        #TODO add duplicates rules
        try:
            queries.add_location_point(id, h, m, s, real_latitude, real_longitude)
        except IntegrityError: #if no id of movable object here
            continue
        counter += 1
    return counter


def upload_points(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_content = request.FILES['file'].read()
            counter = handle_file(file_content)
            return render_to_response("admin/upload_points.html", {'message': u'Из файла успешно добавлено строчек: %d' % counter})
    else:
        form = forms.UploadFileForm()
    return render_to_response("admin/upload_points.html", {'form': form})



