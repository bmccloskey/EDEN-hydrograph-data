# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

from dj_eden_app.models import Station
from dj_eden_app.forms import TimeSeriesFilterForm
import dj_eden_app.data_queries as data_queries

import logging

# Get an instance of a logger
_logger = logging.getLogger(__name__)

import dj_eden_app.stage_data as stage_data
import dj_eden_app.hydrograph as hydrograph
from dj_eden_app.download_header import create_metadata_header
from dj_eden_app.eden_headers import HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER

def timeseries_csv_download(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if (form.is_valid()):
        gages = form.cleaned_data['site_list']
        _logger.info("csv download, gages is %s" % (gages))
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        station_qs = Station.objects.filter(station_name_web__in=gages)

        query_metadata_list = create_metadata_header(HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER, form.cleaned_data, station_qs)

        response = HttpResponse(content_type='text/csv')

        results = stage_data.data_for_download(
                        gages,
                        beginDate=beginDate,
                        endDate=endDate
                    )
        stage_data.write_rdb(results, response, metadata=query_metadata_list)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def hourly_download(request):
    form = TimeSeriesFilterForm(request.GET)

    if (form.is_valid()):
        gages = form.cleaned_data['site_list']
        _logger.info("hourly csv download, gages is %s" % (gages))
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        station_dict = data_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = data_queries.hourly_query(*station_dict.values())
        if beginDate:
            q = q.where(dt >= beginDate)
        if endDate:
            q = q.where(dt <= endDate)
        data = q.execute()

        # data_type = 'Hourly Water Level, NAVD88(ft)'  # hard coded for now... maybe this could be in the form where the user's can selected between hourly and daily data
        query_metadata_list = create_metadata_header(HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER, form.cleaned_data, station_dict.values())

        response = HttpResponse(content_type='text/csv')

        stage_data.write_rdb(data, response, metadata=query_metadata_list)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def daily_download(request):
    form = TimeSeriesFilterForm(request.GET)

    if (form.is_valid()):
        gages = form.cleaned_data['site_list']
        _logger.info("hourly csv download, gages is %s" % (gages))
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        station_dict = data_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = data_queries.daily_query(*station_dict.values())
        if beginDate:
            q = q.where(dt >= beginDate)
        if endDate:
            q = q.where(dt <= endDate)
        data = q.execute()

        # data_type = 'Hourly Water Level, NAVD88(ft)'  # hard coded for now... maybe this could be in the form where the user's can selected between hourly and daily data
        query_metadata_list = create_metadata_header(HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER, form.cleaned_data, station_dict.values())

        response = HttpResponse(content_type='text/csv')

        stage_data.write_rdb(data, response, metadata=query_metadata_list)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))
    pass

# deprecated
def plot_data(request):
    # TODO Pull gage list up to list of model objects
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        _logger.info("plot_data, gages is %s" % (gages))

        station_dict = data_queries.station_dict(gages)

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

        stage_data.write_csv_for_plot(results=data, outfile=response)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_data_auto(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        if days_diff(beginDate, endDate) < 60:
            return plot_data_hourly(request)
        else:
            return plot_data_daily(request)
    else:
        return HttpResponseBadRequest(",".join(form.errors))


def plot_data_hourly(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        _logger.info("plot_data, gages is %s" % (gages))

        station_dict = data_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = data_queries.hourly_query_split(*station_dict.values())
        if beginDate:
            q = q.where(dt >= beginDate)
        if endDate:
            q = q.where(dt <= endDate)
        data = q.execute()

        response = HttpResponse(content_type='text/csv')
        stage_data.write_csv_for_plot(results=data, outfile=response)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_data_daily(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        _logger.info("plot_data, gages is %s" % (gages))

        station_dict = data_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = data_queries.daily_query_split(*station_dict.values())
        if beginDate:
            q = q.where(dt >= beginDate)
        if endDate:
            q = q.where(dt <= endDate)
        data = q.execute()

        response = HttpResponse(content_type='text/csv')
        stage_data.write_csv_for_plot(results=data, outfile=response)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def _daily_plot_data(form):
    gages = form.cleaned_data['site_list']
    _logger.info("plot_data, gages is %s" % (gages))
    station_dict = data_queries.station_dict(gages)
    station1 = station_dict.values()[0]
    beginDate = form.cleaned_data["timeseries_start"]
    endDate = form.cleaned_data["timeseries_end"]
    q, dt = data_queries.daily_query_split(*station_dict.values())
    if beginDate:
        q = q.where(dt >= beginDate)
    if endDate:
        q = q.where(dt <= endDate)
    data = q.execute()
    return data, beginDate, endDate, station1

def _hourly_plot_data(form):
    gages = form.cleaned_data['site_list']
    _logger.info("plot_data, gages is %s" % (gages))
    station_dict = data_queries.station_dict(gages)
    station1 = station_dict.values()[0]

    beginDate = form.cleaned_data["timeseries_start"]
    endDate = form.cleaned_data["timeseries_end"]
    q, dt = data_queries.hourly_query_split(*station_dict.values())
    if beginDate:
        q = q.where(dt >= beginDate)
    if endDate:
        q = q.where(dt <= endDate)
    data = q.execute()
    return data, beginDate, endDate, station1

# Auto select the data to deliver according to size of request input

def days_diff(beginDate, endDate):
    if beginDate is not None and endDate is not None:
        timediff = endDate - beginDate
        return timediff.days
    return None

def plot_image_auto(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        _logger.debug("Image for gages %s", gages)

        if days_diff(beginDate, endDate) < 30:
            if len(gages) == 1:
                return plot_image_hourly_single(request)
            else:
                return plot_image_hourly_multi(request)
        else:
            if len(gages) == 1:
                return plot_image_daily_single(request)
            else:
                return plot_image_daily_multi(request)
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_hourly_multi(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, _ = _hourly_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_multi(data, response, beginDate, endDate)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_hourly_single(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, station = _hourly_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_single_station(data, response, station, beginDate=beginDate, endDate=endDate)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_daily_multi(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, _ = _daily_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_multi(data, response, beginDate, endDate)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_daily_single(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, station = _daily_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_single_station(data, response, station, beginDate=beginDate, endDate=endDate)

        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

