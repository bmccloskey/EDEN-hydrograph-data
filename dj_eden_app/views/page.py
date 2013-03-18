# Create your views here.


from django.shortcuts import render
from django.utils.safestring import mark_safe
import dj_eden_app.data_queries as data_queries

# from .. models import Station
from .. forms import TimeSeriesFilterForm
import logging

# Get an instance of a logger
_logger = logging.getLogger(__name__)

import urllib

def dygraph_series_options(gages):
    '''
    return a JavaScript map for per-series options
    '''
    opt = "{"
    # there are two funky series for each gage: name + est, name + dry

    for gage in gages:
        name = gage
        opt += "'" + name + " est'" + ":{ strokePattern: Dygraph.DOTTED_LINE },\n"
        opt += "'" + name + " dry'" + ":{ strokePattern: Dygraph.DASHED_LINE },\n"
    opt += "'datetime': {}\n"  # IE-safe last element
    opt += '}\n'
    return opt

def to_js_array(seq):
    return "[" + ",".join(seq) + "]"

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

            if query_form.cleaned_data['timeseries_start']:
                str_tstart = '%s' % query_form.cleaned_data['timeseries_start']
            else:
                str_tstart = None

            if query_form.cleaned_data['timeseries_end']:
                str_tend = '%s' % query_form.cleaned_data['timeseries_end']
            else:
                str_tend = None
                
            if query_form.cleaned_data['timeseries_start'] and query_form.cleaned_data['timeseries_end']:
                time_delta = query_form.cleaned_data['timeseries_end'] - query_form.cleaned_data['timeseries_start']
                time_delta_days = time_delta.days
                
            gages = query_form.cleaned_data['site_list']
            render_params = {'query_form': query_form,
                                                   'plot_params': mark_safe(plot_query_str),
                                                   'series_options': mark_safe(dygraph_series_options(gages)),
                                                   'str_tstart': str_tstart,
                                                   'gages':gages,
                                                   'str_tend': str_tend, 
                                                   'time_delta': time_delta_days,}
            if len(gages) == 1:
                station = data_queries.station_list(gages)[0]

                render_params['dry_elevation'] = station.dry_elevation or "null"
                render_params['ground_elevation'] = station.duration_elevation or "null"
            else:
                render_params['dry_elevation'] = "null"
                render_params['ground_elevation'] = "null"

            return render(request, template_name, render_params)
    else:
        pass

    return render (request, template_name, {'query_form': query_form, })
