# Create your views here.


from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import dj_eden_app.stage_queries as stage_queries
from dj_eden_app.colors import ColorRange
from django.conf import settings
from dj_eden_app.plottable import Plottable, NoData

import json

# from .. models import Station
from .. forms import TimeSeriesFilterForm, DataParamForm

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
    if len(gages) == 1:
        ngvd29_name = '%s%s' % (name, '_NGVD29')
        opt += "'%s': { axis:'y2' }, \n" % ngvd29_name
    opt += "'datetime': {}\n"  # IE-safe last element
    opt += '}\n'
    return opt

def to_js_array(seq):
    return "[" + ",".join(seq) + "]"

def eden_base_page(request):
    render_params = {'EDEN_URL': settings.EDEN_URL }
    return render(request, 'eden-base.html', render_params)

def param_page(request):
    template_name = 'eve_params.html'
    param_form = DataParamForm()

    if "clear_form" in request.REQUEST:
        return redirect(param_page)

    has_data = False
    # be careful about initial get with no parameters,
    # so we don't clobber the initial values
    if request.method == 'GET' and request.GET :
        param_form = DataParamForm(request.GET)
        has_data = True
    elif request.method == 'POST':
        param_form = DataParamForm(request.POST)
        has_data = True

    if has_data:
        if param_form.is_valid():
            # Avoid the troublesome Nones.
            plot_params = {}
            for k, v in param_form.cleaned_data.items():
                if v:
                    plot_params[k] = v

            kwargs = {
                      'beginDate' : param_form.cleaned_data['timeseries_start'],
                      'endDate'   : param_form.cleaned_data['timeseries_end']
                      }

            plottables = []
            station_list = stage_queries.station_list([param_form.cleaned_data['site_list']])
            for s in station_list:
                for p in param_form.cleaned_data['params']:
                    pt = Plottable(s, p, **kwargs)
                    plottables.append(pt)

            render_params = {'param_form': param_form,
                             'plottables': plottables,
                             'EDEN_URL': settings.EDEN_URL,
                             }
            return render (request, template_name, render_params)

        else:
            # error in input
            return render(request, template_name, {'param_form': param_form, 'EDEN_URL': settings.EDEN_URL }, status=400)

    return render (request, template_name, {'param_form': param_form, 'EDEN_URL': settings.EDEN_URL })

def eden_page(request):
    """
    Allows a user to select a site,
    date in order to view a dygraph
    plot of results.
    """

    # TODO If URL does not end with /, redirect there for ease of form generation

    template_name = 'eve.html'
    query_form = TimeSeriesFilterForm()

    eden_url = settings.EDEN_URL

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
        """
        if not query_form.has_changed():
            return render(request, template_name, {'query_form': query_form, })
        """
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

            gages = query_form.cleaned_data['site_list']
            colors = ColorRange(count=len(gages))

            _logger.debug("In page generation, colors = %s", list(colors))

            render_params = {'query_form': query_form,
                                                   'plot_params': mark_safe(plot_query_str),
                                                   'series_options': mark_safe(dygraph_series_options(gages)),
                                                   'str_tstart': str_tstart,
                                                   'gages':gages,
                                                   'str_tend': str_tend,
                                                   'colors': mark_safe(json.dumps(list(colors))),
                                                   'color_list': list(colors),
                                                   'DYGRAPH_RANGE_SELECTOR':settings.DYGRAPH_RANGE_SELECTOR,
                                                   'EDEN_URL': eden_url,
			}
            if len(gages) == 1:
                station = stage_queries.station_list(gages)[0]
                render_params['ngvd29_series'] = '%s%s' % (station.station_name_web, '_NGVD29')
                render_params['dry_elevation'] = station.dry_elevation or "null"
                render_params['ground_elevation'] = station.duration_elevation or "null"
                render_params['ngvd29_correction'] = station.vertical_conversion or 0.0
            else:
                render_params['dry_elevation'] = "null"
                render_params['ground_elevation'] = "null"
                render_params['ngvd29_correction'] = "null"

            return render(request, template_name, render_params)
        else:
            return render(request, template_name, {'query_form': query_form, 'EDEN_URL': eden_url}, status=400)

    return render(request, template_name, {'query_form': query_form, 'EDEN_URL': eden_url})
