# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe

from forms import TimeSeriesFilterForm

import stage_data
import exceptions
import urllib
import hydrograph

def timeseries_csv_download(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if (form.is_valid()):
        gages = form.cleaned_data['site_list']
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
        return HttpResponseBadRequest(form.errors)


def plot_data(request):
    # TODO Pull gage list up to list of model objects
    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        maxCount = form.cleaned_data["max_count"]

        response = HttpResponse(content_type='text/csv')

        results = stage_data.data_for_plot(gages,
                                       beginDate=beginDate,
                                       endDate=endDate,
                                       maxCount=maxCount
                                       )
        stage_data.write_csv(results, response)
        return response
    else:
        return HttpResponseBadRequest(form.errors)

def plot_image(request):
    # TODO Pull gage list up to list of model objects

    form = TimeSeriesFilterForm(request.GET)

    if form.is_valid():
        gages = form.cleaned_data['site_list']
        beginDate = form.cleaned_data["timeseries_start"]
        endDate = form.cleaned_data["timeseries_end"]
        maxCount = form.cleaned_data["max_count"]

        response = HttpResponse(content_type='image/png')

        hydrograph.png(gages, response,
                   beginDate=beginDate,
                   endDate=endDate,
                   maxCount=maxCount
                   )

        return response
    else:
        return HttpResponseBadRequest(form.errors)

def eden_page(request):
    """
    Allows a user to select a site,
    date in order to view a dygraph
    plot of results.
    """

    template_name = 'hydrograph_query.html'
    query_form = TimeSeriesFilterForm()

    if request.method == 'GET':
        query_form = TimeSeriesFilterForm(request.GET)

        if not query_form.has_changed():
            return render(request, template_name, {'query_form': query_form, })

        if query_form.is_valid():

            # Avoid the troublesome Nones.
            plot_params = {}
            for k, v in query_form.cleaned_data.items():
                if v:
                    plot_params[k] = v

            plot_param_str = urllib.urlencode(plot_params, doseq=True);

            return render(request, template_name, {'query_form': query_form,
                                                      'plot_params': mark_safe(plot_param_str)})
    else:
        pass

    return render (request, template_name, {'query_form': query_form, })
