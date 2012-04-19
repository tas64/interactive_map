from django.conf.urls.defaults import *
from django.contrib import admin

import settings

from imap import views

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),

    (r'^site-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^db_test/', views.db_connection_test),

    #ajaxtest queries
    (r'^ajaxtest/simple/$', views.simple_ajax_request),
    (r'^ajaxtest/movables/$', views.movables_objects),
    (r'^ajaxtest/immobile/$', views.immobiles_objects),
    (r'^ajaxtest/location_points/(\d+)/$', views.location_points_for),
    (r'^ajaxtest/$', views.ajaxtest),

    #maps api test
    (r'^mapsapi/$', views.mapsapi),


    (r'^$', views.main)
)
