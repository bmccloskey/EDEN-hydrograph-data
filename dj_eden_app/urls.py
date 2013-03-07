from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('dj_eden_app.views',
                      url(r'^timeseries/$', 'eden_page', name='eden_timeseries'),
                      url(r'^data_download/$', 'timeseries_csv_download', name='timeseries_download') 
    # Examples:
    # url(r'^$', 'eden_example.views.home', name='home'),
    # url(r'^eden_example/', include('eden_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
