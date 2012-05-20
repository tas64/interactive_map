from django.conf.urls.defaults import *
from django.contrib import admin
from imap.views.admin import views

import settings

from imap.views import main_view, ajax_views, test_views

admin.autodiscover()

urlpatterns = patterns('',
    #pages of site
    (r'^$', main_view.main),

    (r'^admin/', include('server.imap.views.admin.urls')),

    #ajax queries
    (r'^ajax/simple/$', ajax_views.simple_request),
    (r'^ajax/movables/$', ajax_views.movables_objects),
    (r'^ajax/immobile/$', ajax_views.immobiles_objects),
    (r'^ajax/location_points/(\d+)/$', ajax_views.location_points_for),
    (r'^ajax/del_location_points/(\d+)/$', ajax_views.del_location_points_for),
    (r'^ajax/save_location_points/(\d+)/$', ajax_views.save_location_points_for),



    #test pages
    (r'^test/ajaxtest/$', test_views.ajaxtest),
    (r'^test/mapsapi/$', test_views.mapsapi),
    (r'^test/immobiles/$', test_views.all_immobiles_on_map),
    (r'^test/db/$', test_views.db_connection_test),

    #service queries
    (r'^django/', include(admin.site.urls)),
    (r'^site-media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),


)
