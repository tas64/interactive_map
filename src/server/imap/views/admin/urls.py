# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$', views.main_page),
    (r'^immobiles/$', views.show_immobiles),
    (r'^immobiles/del/(\d+)/$', views.del_immobile),
    (r'^immobiles/add/$', views.add_immobile),
    (r'^immobiles/edit/(\d+)/$', views.edit_immobile),

)