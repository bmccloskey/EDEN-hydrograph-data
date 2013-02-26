from django.forms import Form, DateTimeField, MultipleChoiceField, SelectMultiple
from models import Station


def convert_qs_to_list(qs):
    '''
    creates a list which is used for the multiselect list
    on the application. The "str_object" is the site name
    used for queries in views.py, while "display_str" is
    the display name on the web page.
    '''
    
    choice_list = []
    for qs_object in qs:
        str_object = str(qs_object)
        display_str = str_object.replace('_', ' ')
        site_tuple = (str_object, display_str)
        choice_list.append(site_tuple)
        
    return choice_list

class TimeSeriesFilterForm(Form):
    
    queryset = Station.objects.filter(edenmaster_start__isnull = False).order_by('station_name_web') # returns stations where data collection has started
    
    timeseries_start = DateTimeField(required = True)
    timeseries_end = DateTimeField(required = True)
    site_list = MultipleChoiceField(choices = convert_qs_to_list(queryset), 
                                    required = True, 
                                    widget = SelectMultiple(attrs={'size':'25'}))