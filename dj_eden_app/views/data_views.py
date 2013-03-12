# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

from .. models import Station
from .. forms import TimeSeriesFilterForm
from sqlalchemy.sql.functions import min, max
from sqlalchemy.sql import func
import logging

# Get an instance of a logger
_logger = logging.getLogger(__name__)

from .. import stage_data
from .. import hydrograph

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

        data = stage_data.data_for_plot(gages,
                                        beginDate=beginDate,
                                        endDate=endDate,
                                        maxCount=maxCount,
                                        station_dict=station_dict
                                        )

        stage_data.write_csv(data, response)
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
