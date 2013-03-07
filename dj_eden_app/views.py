# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from forms import TimeSeriesFilterForm

import stage_data
import exceptions
import urllib
import hydrograph

def timeseries_csv_download(request):
    # TODO Pull gage list up to list of model objects
    # TODO use form or inline fields to validate input
    gages = request.GET.getlist("gage")
    beginDate = request.GET.get("beginDate")
    endDate = request.GET.get("endDate")

    response = HttpResponse(content_type='text/csv')

    results = stage_data.data_for_download(gages,
                                       beginDate=beginDate,
                                       endDate=endDate
                                       )
    stage_data.write_csv(results, response)
    return response

def plot_data(request):
    # TODO Pull gage list up to list of model objects
    # TODO use form or inline fields to validate input
    gages = request.GET.getlist("gage")
    beginDate = request.GET.get("beginDate")
    endDate = request.GET.get("endDate")
    try:
        maxCount = int(request.GET.get("maxCount"))
    except (exceptions.ValueError, exceptions.TypeError):
        maxCount = None
    response = HttpResponse(content_type='text/csv')

    results = stage_data.data_for_plot(gages,
                                       beginDate=beginDate,
                                       endDate=endDate,
                                       maxCount=maxCount
                                       )
    stage_data.write_csv(results, response)
    return response

def plot_image(request):
    # TODO Pull gage list up to list of model objects
    # TODO use form or inline fields to validate input
    gages = request.GET.getlist("gage")
    beginDate = request.GET.get("beginDate")
    endDate = request.GET.get("endDate")
    try:
        maxCount = int(request.GET.get("maxCount"))
    except (exceptions.ValueError, exceptions.TypeError):
        maxCount = None

    response = HttpResponse(content_type='image/png')

    hydrograph.png(gages, response,
                   beginDate=beginDate,
                   endDate=endDate,
                   maxCount=maxCount
    )

    return response

def eden_page(request):
    """
    Allows a user to select a site,
    date in order to view a dygraph
    plot of results.
    """

    template_name = 'hydrograph_query.html'

    if request.method == 'GET':
        query_form = TimeSeriesFilterForm(request.GET)

        if not query_form.has_changed():
            return render(request, template_name, {'query_form': query_form, })

        if query_form.is_bound:
            if query_form.is_valid():

                time_start = query_form.cleaned_data['timeseries_start']
                time_end = query_form.cleaned_data['timeseries_end']
                eden_station = query_form.cleaned_data['site_list']

                plot_params = { 'gage':eden_station }
                if time_start:
                    plot_params['beginDate'] = time_start
                if time_end:
                    plot_params['endDate'] = time_end

                plot_param_str = urllib.urlencode(plot_params, doseq=True);

                return render(request, template_name, {'query_form': query_form,
                                                      'plot_params': mark_safe(plot_param_str)})
    else:
        query_form = TimeSeriesFilterForm()
    return render (request, template_name, {'query_form': query_form, })
