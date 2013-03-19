from django.forms import Form, DateField, MultipleChoiceField, SelectMultiple, IntegerField
from models import Station
import datetime

def convert_qs_to_list(qs):
    """
    creates a list of tuples which is used for the multi-select list
    on the application. The "str_object" is the site name
    used for queries in views.py, while "display_str" is
    the display name on the web page.
    """

    # TODO Might prefer to use primary key?
    choice_list = []
    for qs_object in qs:
        str_object = str(qs_object)
        display_str = str_object.replace('_', ' ')
        site_tuple = (str_object, display_str)
        choice_list.append(site_tuple)

    return choice_list

def convert_qs_to_list_of_tuples(qs):
    choice_list = [ (mod_obj.station_id,
                     mod_obj.station_name_web.replace('_', ' '))
                   for mod_obj in qs]
    return choice_list

class TimeSeriesFilterForm(Form):

    #queryset = Station.objects.filter(edenmaster_start__isnull=False).order_by('station_name_web')  # returns stations where data collection has started
    queryset = Station.objects.all().order_by('station_name_web') 
    today = datetime.date.today()
    timeseries_start = DateField(required=False, initial=today.replace(year=today.year - 1))
    timeseries_end = DateField(required=False, initial=today)
    site_list = MultipleChoiceField(choices=convert_qs_to_list(queryset),
                                    required=True,
                                    widget=SelectMultiple(attrs={'size':'25'}))
    max_count = IntegerField(required=False)
