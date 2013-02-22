from django.forms import Form, DateTimeField, ModelChoiceField
from models import Station

class TimeSeriesFilterForm(Form):
    
    timeseries_start = DateTimeField(required = True)
    timeseries_end = DateTimeField(required = True)
    site_list = ModelChoiceField(queryset = Station.objects.all().order_by('station_name'),
                                 empty_label = 'Select sites',
                                 required = True)