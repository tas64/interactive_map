# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.main_page),

    (r'^immobiles/$', views.show_immobiles),
    (r'^immobiles/del/(\d+)/$', views.del_immobile),
    (r'^immobiles/add/$', views.add_immobile),
    (r'^immobiles/edit/(\d+)/$', views.edit_immobile),

    (r'^movables/$', views.show_movables),
    (r'^movables/del/(\d+)/$', views.del_movable),
    (r'^movables/add/$', views.add_movable),
    (r'^movables/edit/(\d+)/$', views.edit_movable),

    (r'^movable_types/$', views.show_movable_types),
    (r'^movable_types/del/(\d+)/$', views.del_movable_type),
    (r'^movable_types/add/$', views.add_movable_type),
    (r'^movable_types/edit/(\d+)/$', views.edit_movable_type),

    (r'^upload_points/$', views.upload_points),


)