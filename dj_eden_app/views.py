# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe

from models import Station
from forms import TimeSeriesFilterForm
import logging

# Get an instance of a logger
_logger = logging.getLogger(__name__)

import stage_data
import urllib
import hydrograph

def timeseries_csv_download(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if (form.is_valid()):
        gages = form.cleaned_data['site_list']
        _logger.info("csv download, gages is %s" % (gages))
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        response = HttpResponse(content_type='text/csv')

        results = stage_data.data_for_download(
                        gages,
                        beginDate=beginDate,
                        endDate=endDate
                    )
        stage_data.write_csv(results, response)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def _station_dict(gages):
    # pull station name list up to Station objects
    stations = Station.objects.filter(station_name_web__in=gages)
    # and make a dictionary mapping names back to stations
    station_dict = dict((s.station_name_web, s) for s in stations)

    return station_dict

def plot_data(request):
    # TODO Pull gage list up to list of model objects
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        _logger.info("plot_data, gages is %s" % (gages))

        station_dict = _station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        maxCount = form.cleaned_data["max_count"]

        response = HttpResponse(content_type='text/csv')

        results = stage_data.data_for_plot(gages,
                                       beginDate=beginDate,
                                       endDate=endDate,
                                       maxCount=maxCount,
                                       station_dict=station_dict
                                       )
        stage_data.write_csv(results, response)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        maxCount = form.cleaned_data["max_count"]

        station_dict = _station_dict(gages)

        response = HttpResponse(content_type='image/png')

        hydrograph.png(gages, response,
                   beginDate=beginDate,
                   endDate=endDate,
                   maxCount=maxCount,
                   station_dict=station_dict
                   )

        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def eden_page(request):
    """
    Allows a user to select a site,
    date in order to view a dygraph
    plot of results.
    """

    # TODO If URL does not end with /, redirect there for ease of form generation

    template_name = 'hydrograph_query.html'
    query_form = TimeSeriesFilterForm()

    has_data = False
    # be careful about initial get with no parameters,
    # so we don't clobber the initial values
    if request.method == 'GET' and request.GET :
        query_form = TimeSeriesFilterForm(request.GET)
        has_data = True
    elif request.method == 'POST':
        query_form = TimeSeriesFilterForm(request.POST)
        has_data = True

    if has_data:
        if not query_form.has_changed():
            return render(request, template_name, {'query_form': query_form, })

        if query_form.is_valid():

            # Avoid the troublesome Nones.
            plot_params = {}
            for k, v in query_form.cleaned_data.items():
                if v:
                    plot_params[k] = v

            plot_query_str = urllib.urlencode(plot_params, doseq=True);

            return render(request, template_name, {'query_form': query_form,
                                                      'plot_params': mark_safe(plot_query_str)})
    else:
        pass

    return render (request, template_name, {'query_form': query_form, })
