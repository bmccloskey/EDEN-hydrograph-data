from django.conf.urls import patterns, include, url
from django.conf import settings
import dj_eden_app.views.data_views as data_views
import dj_eden_app.views.page as page_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^plot_data$', data_views.plot_data),
                       url(r'^plot_data_auto', data_views.plot_data_auto),
                       url(r'^daily_plot_data', data_views.plot_data_daily),
                       url(r'^hourly_plot_data', data_views.plot_data_hourly),
                       url(r'^plot_image$', data_views.plot_image_auto),
                       # Could use URL decomposition to match file-like URL for images
                       url(r'^plot_image_simple$', data_views.plot_image_simple, name="plot_image_simple"),
                       url(r'plot/([^/]+)/(\w+)\.(\w+)', data_views.plot_image, name="plot_image_rest"),

                       url(r'^daily_data_download$', data_views.daily_download),
                       url(r'^hourly_data_download$', data_views.hourly_download),
                       url(r'^data_download$', data_views.timeseries_csv_download),
                       url(r'^param_data_download', data_views.param_data_download, name="param_data_download"),
                       url(r'^param_rdb_download', data_views.param_rdb_download, name="param_rdb_download"),

                       url(r'^eden-base.html$', page_views.eden_base_page),
                       url(r'^timeseries/?$', page_views.eden_page, name='eden_timeseries'),
                       url(r'^eve.html/?$', page_views.eden_page, name='eve'),
                       url(r'^eve_params.html/?$', page_views.param_page),

    # Examples:
    # url(r'^$', 'eden_example.views.home', name='home'),
    # url(r'^eden_example/', include('eden_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
