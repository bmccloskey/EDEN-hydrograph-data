# Create your views here.


from django.shortcuts import render
from django.utils.safestring import mark_safe

# from .. models import Station
from .. forms import TimeSeriesFilterForm
import logging

# Get an instance of a logger
_logger = logging.getLogger(__name__)

import urllib

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

            return render(request, template_name, {'query_form': query_form,
                                                   'plot_params': mark_safe(plot_query_str),
                                                   'str_tstart': str_tstart,
                                                   'str_tend': str_tend,})
    else:
        pass

    return render (request, template_name, {'query_form': query_form, })
