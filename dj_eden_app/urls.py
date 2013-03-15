from django.conf.urls import patterns, include, url
from django.conf import settings
import dj_eden_app.views.data_views as data_views
import dj_eden_app.views.page as page_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^plot_data$', data_views.plot_data),
                       url(r'^daily_plot_data', data_views.plot_data_daily),
                       url(r'^hourly_plot_data', data_views.plot_data_hourly),
                       url(r'^plot_image$', data_views.plot_image),
                       url(r'^data_download$', data_views.timeseries_csv_download),
                       url(r'^timeseries/?$', page_views.eden_page, name='eden_timeseries'),
    # Examples:
    # url(r'^$', 'eden_example.views.home', name='home'),
    # url(r'^eden_example/', include('eden_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
