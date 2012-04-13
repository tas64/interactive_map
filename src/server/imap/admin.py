# -*- coding: utf-8 -*-

from django.contrib import admin
from models import MovableObject, ImmobileObject, LocationPoint

class MovableObjectAdmin(admin.ModelAdmin):
#    search_fields = ('name', )
    list_display = ('id', 'name', 'type')
#    list_filter = ('credit',)
    fields = ('name', 'type')
    list_per_page = 30

class ImmobileObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'latitude_degree', 'latitude_minute', 'is_north',
                    'longitude_degree', 'longitude_minute', 'is_east')
    fields = list_display[1:]
    list_per_page = 30

class LocationPointAdmin(admin.ModelAdmin):
    list_display = ('movable_object', 'hour', 'minute', 'second', 'latitude_degree', 'latitude_minute', 'is_north',
                    'longitude_degree', 'longitude_minute', 'is_east')
    fields = list_display
    list_per_page = 30


admin.site.register(MovableObject, MovableObjectAdmin)
admin.site.register(ImmobileObject, ImmobileObjectAdmin)
admin.site.register(LocationPoint, LocationPointAdmin)
