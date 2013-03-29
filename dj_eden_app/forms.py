from django.forms import Form, DateField, MultipleChoiceField, SelectMultiple, DateInput, IntegerField, ValidationError
from models import Station
import datetime

def convert_qs_to_list_of_tuples(qs):
    """
    creates a list of tuples which is used for the multi-select list
    on the application. The first element is the key, the second is the
    displayed name.
    """
    choice_list = [ (mod_obj.station_name_web,
                     mod_obj.short_name.replace('_', ' '))
                   for mod_obj in qs]
    return choice_list

class TimeSeriesFilterForm(Form):

    queryset = Station.objects.filter(edenmaster_start__isnull=False).order_by('station_name_web')  # returns stations where data collection has started
    today = datetime.date.today()
    timeseries_start = DateField(required=False,
                                 initial=today.replace(year=today.year - 1),
                                 widget=DateInput(attrs={"size":"10"}))
    timeseries_end = DateField(required=False,
                               initial=today,
                               widget=DateInput(attrs={"size":"10"}))
    site_list = MultipleChoiceField(choices=convert_qs_to_list_of_tuples(queryset),
                                    required=True,
                                    widget=SelectMultiple(attrs={'size':'20'}))
    max_count = IntegerField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        t_start = cleaned_data.get('timeseries_start')
        t_end = cleaned_data.get('timeseries_end')
        
        if t_start != None and t_end != None:
            if t_start > t_end:
                raise ValidationError('Please enter a start date that precedes the end date.')
        else:
            pass
        
        return cleaned_data
 
            
