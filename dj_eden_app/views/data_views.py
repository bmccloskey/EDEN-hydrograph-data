# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

from dj_eden_app.models import Station
from dj_eden_app.forms import TimeSeriesFilterForm, DataParamForm
import dj_eden_app.stage_queries as stage_queries
from dj_eden_app.plottable import Plottable

import logging
import sys

# Get an instance of a logger
_logger = logging.getLogger(__name__)

import dj_eden_app.stage_data as stage_data
import dj_eden_app.hydrograph as hydrograph
from dj_eden_app.download_header import create_metadata_header
from dj_eden_app.eden_headers import HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER

_default_show_logo = not 'windows' in sys.platform

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

        station_dict = stage_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = stage_queries.hourly_query(*station_dict.values())
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

        station_dict = stage_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = stage_queries.daily_query(*station_dict.values())
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

        station_dict = stage_queries.station_dict(gages)

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


def param_rdb_download(request):
    form = DataParamForm(request.GET)
    if form.is_valid():
        _logger.info("requested data download for %s with params %s" % (form.cleaned_data['site_list'], form.cleaned_data['params']))

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        gage = form.cleaned_data['site_list']
        p = form.cleaned_data['params'][0]

        station_list = stage_queries.station_list([str(gage)])
        pt = Plottable(station_list[0], p, beginDate, endDate)
        data_seq = pt.sequence()

        # fifth parameter to create_metadata_header is list of Station objects
        station_list = stage_queries.station_list([gage])
        query_metadata_list = create_metadata_header(HEADER_MESSAGE, EDEN_CONTACT, END_OF_HEADER, form.cleaned_data, station_list)

        response = HttpResponse(content_type='text/csv')
        stage_data.write_rdb(data_seq, response, metadata=query_metadata_list)

        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def param_data_download(request):

    form = DataParamForm(request.GET)
    if form.is_valid():
        _logger.info("requested plot data for %s with params %s" % (form.cleaned_data['site_list'], form.cleaned_data['params']))

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        gage = form.cleaned_data['site_list']
        p = form.cleaned_data['params'][0]

        station_list = stage_queries.station_list([gage])
        pt = Plottable(station_list[0], p, beginDate, endDate)

        data_seq = pt.sequence()

        response = HttpResponse(content_type='text/csv')
        stage_data.write_csv(data_seq, response)

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

        station_dict = stage_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = stage_queries.hourly_query_split(*station_dict.values())
        if beginDate:
            q = q.where(dt >= beginDate)
        if endDate:
            q = q.where(dt <= endDate)
        data = q.execute()

        if len(gages) == 1:
            site_name = '%s_NGVD29' % gages[0]
        else:
            site_name = None

        response = HttpResponse(content_type='text/csv')
        stage_data.write_csv_for_plot(results=data, outfile=response, column_name=site_name)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_data_daily(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        _logger.info("plot_data, gages is %s" % (gages))

        station_dict = stage_queries.station_dict(gages)

        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]

        q, dt = stage_queries.daily_query_split(*station_dict.values())
        if beginDate:
            q = q.where(dt >= beginDate)
        if endDate:
            q = q.where(dt <= endDate)
        data = q.execute()

        response = HttpResponse(content_type='text/csv')
        if len(gages) == 1:
            site_name = '%s_NGVD29' % gages[0]
        else:
            site_name = None
        # stage_data.write_csv(results=data, outfile=response, station_name=site_name)
        stage_data.write_csv_for_plot(results=data, outfile=response, column_name=site_name)
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def _daily_plot_data(form):
    gages = form.cleaned_data['site_list']
    _logger.info("plot_data, gages is %s" % (gages))
    station_dict = stage_queries.station_dict(gages)
    station1 = station_dict.values()[0]
    beginDate = form.cleaned_data["timeseries_start"]
    endDate = form.cleaned_data["timeseries_end"]
    q, dt = stage_queries.daily_query_split(*station_dict.values())
    if beginDate:
        q = q.where(dt >= beginDate)
    if endDate:
        q = q.where(dt <= endDate)
    data = q.execute()
    return data, beginDate, endDate, station1

def _hourly_plot_data(form):
    gages = form.cleaned_data['site_list']
    _logger.info("plot_data, gages is %s" % (gages))
    station_dict = stage_queries.station_dict(gages)
    station1 = station_dict.values()[0]

    beginDate = form.cleaned_data["timeseries_start"]
    endDate = form.cleaned_data["timeseries_end"]
    q, dt = stage_queries.hourly_query_split(*station_dict.values())
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

def plot_image_simple(request):
    form = DataParamForm(request.GET)

    if form.is_valid():
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        gage = form.cleaned_data['site_list']
        p = form.cleaned_data['params'][0]

        station_list = stage_queries.station_list([str(gage)])
        pt = Plottable(station_list[0], p, beginDate, endDate)

        data_seq = pt.sequence()

        show_logo = decide_logo(request)

        # Let logo also drive title display
        if show_logo:
            title = pt.title()

        response = HttpResponse(content_type='image/png')

        hydrograph.png_simple(data_seq, response, beginDate=beginDate, endDate=endDate,
                              show_logo=show_logo, title=title, y_label=pt.label_y())

        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def decide_logo(request):
        show_logo = _default_show_logo
        if 'no_logo' in request.REQUEST:
                show_logo = False
        return show_logo

def plot_image_hourly_multi(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, _ = _hourly_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_multi(data, response, beginDate, endDate, show_logo=decide_logo(request))
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_hourly_single(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, station = _hourly_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_single_station(data, response, station, beginDate=beginDate, endDate=endDate, show_logo=decide_logo(request))
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_daily_multi(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, _ = _daily_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_multi(data, response, beginDate, endDate, show_logo=decide_logo(request))
        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

def plot_image_daily_single(request):
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        data, beginDate, endDate, station = _daily_plot_data(form)

        response = HttpResponse(content_type='image/png')

        hydrograph.png_single_station(data, response, station, beginDate=beginDate, endDate=endDate, show_logo=decide_logo(request))

        return response
    else:
        return HttpResponseBadRequest(",".join(form.errors))

