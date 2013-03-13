# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

from dj_eden_app.models import Station
from dj_eden_app.forms import TimeSeriesFilterForm
import logging

# Get an instance of a logger
_logger = logging.getLogger(__name__)

import dj_eden_app.stage_data as stage_data
import dj_eden_app.hydrograph as hydrograph
from .. import nwis_rdb

def timeseries_csv_download(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if (form.is_valid()):
        gages = form.cleaned_data['site_list']
        _logger.info("csv download, gages is %s" % (gages))
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        
        query_metadata = nwis_rdb.create_rdf_header(nwis_rdb.HEADER_MESSAGE, nwis_rdb.EDEN_CONTACT, nwis_rdb.END_OF_HEADER, form.cleaned_data)

        response = HttpResponse(content_type='text/csv')

        results = stage_data.data_for_download(
                        gages,
                        beginDate=beginDate,
                        endDate=endDate
                    )
        stage_data.write_csv(results=results, outfile=response, metadata=query_metadata)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def _station_dict(gages):
    # pull station name list up to Station objects
    stations = Station.objects.filter(station_name_web__in=gages)
    # and make a dictionary mapping names back to stations
    station_dict = dict((s.station_name_web, s) for s in stations)

    return station_dict

def station_list(gages):
    value = []
    for g in gages:
        s = Station.objects.get(station_name_web=g)
        value.append(s)
    return value

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

        data = stage_data.data_for_plot(gages,
                                        beginDate=beginDate,
                                        endDate=endDate,
                                        maxCount=maxCount,
                                        station_dict=station_dict
                                        )

        stage_data.write_csv(results=data, outfile=response)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']

        station_dict = _station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        maxCount = form.cleaned_data["max_count"]

        response = HttpResponse(content_type='image/png')

        data = stage_data.data_for_plot(gages,
                                        beginDate=beginDate,
                                        endDate=endDate,
                                        maxCount=maxCount,
                                        station_dict=station_dict
                                        )

        hydrograph.png(data, response, beginDate, endDate)

        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))
