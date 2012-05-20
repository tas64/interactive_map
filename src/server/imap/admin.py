# -*- coding: utf-8 -*-

from django.contrib import admin
from models import MovableObject, ImmobileObject, LocationPoint

class MovableObjectAdmin(admin.ModelAdmin):
#    search_fields = ('name', )
    list_display = ('id', 'name', 'movable_type')
#    list_filter = ('credit',)
    fields = ('name', 'movable_type')
    list_per_page = 30

class ImmobileObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'latitude','longitude')
    fields = list_display[1:]
    list_per_page = 30

class LocationPointAdmin(admin.ModelAdmin):
    list_display = ('movable_object', 'time', 'latitude','longitude')
    fields = list_display
    list_per_page = 30


admin.site.register(MovableObject, MovableObjectAdmin)
admin.site.register(ImmobileObject, ImmobileObjectAdmin)
admin.site.register(LocationPoint, LocationPointAdmin)
